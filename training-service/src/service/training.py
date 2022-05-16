from threading import Lock
import logging
import numpy as np
import os
from src.repository.annotation import AnnotationRepository
from src.repository.model import ModelRepository
import config as config
from src.util.SHModelHelper import from_db_model_to_sh_model, from_best_sh_model_to_db_model

logger = logging.getLogger('waitress')
lock = Lock()
annotation_repository = AnnotationRepository()
model_repository = ModelRepository()
FALLBACK_ACCURACY = 0

def train_models(model="all"):
    """Trains models if there is at least the number of MIN_TRAINING_BATCH_SIZE entries on db collection "annotation".
    
    Returns:
        String, based on which condition is fullfilled.  
    """
    # only one thread can execute code there
    with lock:
        logger.debug(f"[TRAINING] ### TRAINING STARTED with model {model} ### ")
        
        trained_languages = []
        languages_to_train = config.SUPPORTED_LANGUAGES if model == "all" else [model]
        for lang_name in languages_to_train:
            logger.debug(f"[TRAINING] Starting model training for {lang_name}")

            training_data = annotation_repository.find_data_to_train_with(lang_name)
            logger.debug(f"[TRAINING] Training data loaded from DB: {len(training_data)}")

            min_training_batch_size = int(os.environ.get('MIN_TRAINING_BATCH_SIZE'))
            training_data_len = len(training_data)
            if training_data_len < min_training_batch_size:
                logger.debug(f"[TRAINING] Not enough data to train model: training data: {training_data_len}, minimum training batch size: {min_training_batch_size}")
                continue

            annotations_train, annotations_val = split_objects(training_data)
            improve_model(annotations_train, annotations_val, lang_name)
            trained_languages.append(lang_name)

        logger.debug("[TRAINING] ### TRAINING DONE ###")

        if not trained_languages:
            return "No languages trained. Not enough training data."
        return "Models trained for: " + str(trained_languages)


def data_preprocessing(annotation_data):
    """Takes an array of certain dimensions and extracts the lexing and highlighting tokens & separates them.

    Args: 
        Training_data array wich includes lexing and highlighting tokens.
    
    Returns: 
        Two numpy arrays X, T such that the training process can be started with these inputs.
    """
    X = []
    T = []
    for sample in annotation_data:
        X.append(sample.key.lexingTokens)
        T.append(sample.highlightingTokens)
    X = np.array(X, dtype=object)
    T = np.array(T, dtype=object)
    return X, T


def improve_model(annotations_train, annotations_val, lang_name):
    """Fetches best model respectively most recent model from db and converts the db file into SHModel. Then it splits X & T in training, 
    validation and test data. The accuracy is computed before (with validation set) & after (with test set) training the fetched model.
    If accuracy of the fetched model is higher after training than the current used model the new model will be saved to the current directory 
    such that the old model will be overwritten.
    
    Args: 
        Array with lexing tokens (training data) X, array with highlighting tokens (targets) T, string with language name lang_name,
        training_data?
    
    Returns: 
        None, but saves new trained model to db if the new accuracy (after the training process) is higher, than the accuracy of the current model
        which is used by the prediction service.
    """
    #RECALL: return value of split_objects function: annotations_train, annotations_val
    

    # prepare training data
    X_train, T_train = data_preprocessing(annotations_train)
    # prepare validation data
    X_val, T_val = data_preprocessing(annotations_val)
    
    # fetch model from db and convert it from a binary file into an SHModel
    best_db_model = model_repository.find_best_model(lang_name)
    best_sh_model = from_db_model_to_sh_model(best_db_model, lang_name)
    
    # used for comparison later, if no model on db, 0 is returned
    cur_acc = best_db_model.accuracy if best_db_model else FALLBACK_ACCURACY
 
    # train model on training set
    train(best_sh_model, X_train, T_train)
    
    # compute accuracy of model on GLOBAL validation set
    validation_data = annotation_repository.find_validation_data(lang_name)
    logger.debug(f"[TRAINING] Previous validation data from db loaded: {len(validation_data)}")
    if validation_data:
        X_val_previous, T_val_previous = data_preprocessing(validation_data)
        X_val = np.append(X_val, X_val_previous)
        T_val = np.append(T_val, T_val_previous)
    
    # compute accuracy with the entire historic validation dataset
    new_acc = compute_accuracy(best_sh_model, X_val, T_val)
    logger.debug(f"[TRAINING] Validated with {len(X_val)} data")
    
    logger.debug(f"[TRAINING] new_acc = {new_acc} and cur_acc = {cur_acc}")
    if new_acc > cur_acc:
        logger.debug("[SHModel] Persisting model to directory")
        best_sh_model.persist_model()
        improved_db_model = from_best_sh_model_to_db_model(lang_name, new_acc)
        model_repository.save(improved_db_model)
        logger.debug(f"[TRAINING] Flag {len(annotations_train)} as trained data and {len(annotations_val)} as validated data")
        annotation_repository.update_trained_time(annotations_train)
        annotation_repository.update_validated_time(annotations_val)
        return 

    logger.debug("[TRAINING] No improvement: do nothing")


def train(model, X_train, T_train, epochs=10):
    """Trains the model based on a number on epochs. Before the start of the training process, the model will be set into the finetuning mode.
    Training data will be shuffled before the start of the process.
    
    Args:
        An SHModel, two arrays which contain training data and targets, number of epochs (default is 10).

    Returns:
        Array with losses.
    """
    logger.debug("[TRAINING] Model training started...")
    model.setup_for_finetuning()
    avg_epoch_losses = []
    for epoch in range(epochs):
        epoch_losses = []
        X_train, T_train = shuffle_data(X_train, T_train)
        for idx, x in enumerate(X_train):  
            loss = model.finetune_on(x, T_train[idx])
            epoch_losses.append(loss)
                        
        cur_avg_epoch_loss = sum(epoch_losses)/len(epoch_losses)
        avg_epoch_losses.append(cur_avg_epoch_loss)
        logger.debug(f"[TRAINING] Epoch: {epoch+1}/{epochs}, Average Loss {cur_avg_epoch_loss}")
        
        if epoch > 0 and cur_avg_epoch_loss >= avg_epoch_losses[epoch-1]:
            logger.debug(f"[TRAINING] EARLY EPOCH STOPPING: current avg epoch loss {round(cur_avg_epoch_loss, 10)} >= previous avg epoch loss {round(avg_epoch_losses[epoch-1], 10)}")
            break

def shuffle_data(X, T):
    """Shuffles two arrays accordingly. 
    
    Args:
        Two np arrays.
        
    Returns:
        Returns two shuffled np arrays.
    """
    assert len(X) == len(T)
    p = np.random.permutation(len(X))
    return X[p], T[p]


def split_objects(annotations, train_percentage=0.8):
    """ Splits an array of objects into training and validation data.
    Args:
        Arrays with objects from class Annotation. Possibility to define the split of train and test data by the user with parameter train_percentage.
    
    Returns:
       2 arrays with default split of 0.8 training & 0.2 validation data 
    """
    # training data = [ann_objs1, ann_objs2....]
    
    split = int(train_percentage * len(annotations))
    
    annotations_train = annotations[:split]
    annotations_val = annotations[split:]

    return annotations_train, annotations_val


def compute_accuracy(model, X, T):
    """Predicts the accuracy of a model based on the lexing tokens (in X) via the predict() function and compares the output with the target resp.
    the highlighting tokens (in T). If predicted highlighting token equals the highlighting token of the T array the var correct is incremented
    In any case the var total will be incremented. 

    Args:
        SHModel and an array with training data & an array with target.
    
    Returns:
        A value between 0 & 1 due to the divison of correct/total.
"""
    assert X.shape == T.shape
    model.setup_for_prediction()
    correct = 0
    total = 0
    for idx, x in enumerate(X):
        h_codes = model.predict(x)
        for j, h_code in enumerate(h_codes):
            if h_code == T[idx][j]:
                correct += 1
            total += 1

    return correct/total
