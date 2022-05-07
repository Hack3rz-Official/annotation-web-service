import numpy as np
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from src.repository.annotation import AnnotationRepository
from src.repository.model import ModelRepository
import config as config
from src.util.SHModelHelper import from_db_model_to_sh_model, from_best_sh_model_to_db_model

annotation_repository = AnnotationRepository()
model_repository = ModelRepository()
FALLBACK_ACCURACY = 0

def train_models(model="all"):
    """Trains models if there is at least the number of TRAINING_BATCH_SIZE entries on db collection "annotation".
    
    Returns:
        String, based on which condition is fullfilled.  
    """
    print("[TRAIN] ### TRAINING STARTED ### ", flush=True)

    trained_languages = []
    languages_to_train = config.SUPPORTED_LANGUAGES if model == "all" else [model]
    for lang_name in languages_to_train:
        print("[TRAIN] Starting model training for " + lang_name, flush=True)

        training_data = annotation_repository.find_data_to_train_with(lang_name)
        print("[TRAIN] training data loaded from DB: " + str(len(training_data)), flush=True)

        if len(training_data) < int(os.environ.get('TRAINING_BATCH_SIZE')):
            print("[TRAIN] Not enough data to train model", flush=True)
            continue

        annotations_train, annotations_val = split_objects(training_data)
    
        improve_model(annotations_train, annotations_val, lang_name)
        trained_languages.append(lang_name)

    print("[TRAIN] ### TRAINING DONE ### ", flush=True)

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
    print("[TRAIN] validation data loaded from DB: " + str(len(validation_data)), flush=True)
    X_val_previous, T_val_previous = data_preprocessing(validation_data)
    X_val_all = np.append(X_val, X_val_previous)
    T_val_all = np.append(T_val, T_val_previous)
    new_acc = compute_accuracy(best_sh_model, X_val_all, T_val_all)

    print(f"new_acc = {new_acc} and cur_acc = {cur_acc}, ", flush=True)
    if new_acc > cur_acc:
        print("[SHModel] Persisting model to directory ", flush=True)
        best_sh_model.persist_model()
        improved_db_model = from_best_sh_model_to_db_model(lang_name, new_acc)
        model_repository.save(improved_db_model)
        annotation_repository.update_trained_time(annotations_train)
        annotation_repository.update_validated_time(annotations_val)
        return 

    print("[TRAIN] No improvement: do nothing", flush=True)



def train(model, X_train, T_train, epochs=10, error_convergence=0.001):
    """Trains the model based on a number on epochs. Before the start of the training process, the model will be set into the finetuning mode.
    Training data will be shuffled before the start of the process.
    
    Args:
        An SHModel, two arrays which contain training data and targets, number of epochs (default is 10).

    Returns:
        Array with losses.
    """
    model.setup_for_finetuning()
    X_train, T_train = shuffle_data(X_train, T_train)
    losses = np.array([])
    delta = 100
    for epoch in range(epochs):
        print("Epoch: ", epoch+1)
        epoch_losses = np.array([])
        for idx, x in enumerate(X_train):
            if delta < error_convergence:
                break
            loss_of_sample = model.finetune_on(x, T_train[idx])
            if idx != 0:
                delta = epoch_losses[idx-1]-loss_of_sample
                print("current delta: ", delta, flush=True)
            epoch_losses = np.append(epoch_losses, loss_of_sample)
        if delta < error_convergence:
            break
        avg_epoch_loss = np.mean(epoch_losses)
        print(f'Average Loss {avg_epoch_loss} in epoch {epoch+1}', flush=True)  
        losses = np.append(losses, avg_epoch_loss)

          
    return losses


def shuffle_data(X, T):
    """Shuffles two arrays accordingly. 
    
    Args:
        Two np arrays.
        
    Returns:
        Returns two shuffled np arrays.
    
    """
    print("[TRAIN] shuffling data...", flush=True)
    assert len(X) == len(T)
    X, T = shuffle(X, T, random_state=0)
    return X, T



def split_objects(annotations, train_percentage=0.8):
    """ Splits an array of objects into training and validation data.
    Args:
        Arrays with objects from class Annotation. Possibility to define the split of train and test data by the user with parameter train_percentage.
    
    Returns:
       2 arrays with default split of 0.8 training & 0.2 validation data 
    """
    # training data = [ann_objs1, ann_objs2....]
    
    split = int(train_percentage*len(annotations))
    
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
        h_codes = model.predict(x)  # [2,3,4,6]
        for j, h_code in enumerate(h_codes):
            if h_code == T[idx][j]:
                correct += 1
            total += 1

    return correct/total
