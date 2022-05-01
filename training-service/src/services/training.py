import numpy as np
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from src.repositories.annotation import AnnotationRepository
from src.repositories.model import ModelRepository
import config as config
from src.util.SHModelHelper import from_db_model_to_sh_model, from_best_sh_model_to_db_model

annotation_repository = AnnotationRepository()
model_repository = ModelRepository()

"""
fnc which trains models if there is at least the number of TRAINING_BATCH_SIZE rows on db collection "annotation". 
if number of rows < TRAININ_BATCH_size the fnc is terminated.

"""
def train_models():
    print("[TRAIN] ### TRAINING STARTED ### ", flush=True)

    trained_languages = []
    for lang_name in config.SUPPORTED_LANGUAGES:
        print("[TRAIN] Starting model training for " + lang_name, flush=True)

        training_data = annotation_repository.find_training_data(lang_name)
        print("[TRAIN] Training data loaded from DB: " + str(len(training_data)), flush=True)

        if len(training_data) < int(os.environ.get('TRAINING_BATCH_SIZE')):
            print("[TRAIN] Not enough data to train model", flush=True)
            continue

        X, T = data_preprocessing(training_data)
        improve_model(X, T, lang_name, training_data)
        trained_languages.append(lang_name)

    print("[TRAIN] ### TRAINING DONE ### ", flush=True)

    if not trained_languages:
        return "No languages trained. Not enough training data."
    return "Models trained for: " + str(trained_languages)

"""
fnc which takes a parameter called training_data and extracts the lexing and highlighting tokens.
Returns two numpy arrays X, T
"""
def data_preprocessing(training_data):
    X = []
    T = []
    for sample in training_data:
        X.append(sample.key.lexingTokens)
        T.append(sample.highlightingTokens)
    X = np.array(X, dtype=object)
    T = np.array(T, dtype=object)
    return X, T

"""
fnc with params X, T lang_name, and training_data
Splits X & T in training, validation and test data
Fetches best model from db and converts the db file into SH model
Accuracy is computed before (with validation set) & after (with test set) training the fetched model
If accuracy of the fetched model is higher after training than the current used model the new model will be saved to 
the current directory such that the old model will be overwritten
"""
def improve_model(X, T, lang_name, training_data):
    #RECALL: return value of split_data function: X_train, X_val, T_train, T_val
    
    #split the data in 80:10:10 for train:valid:test dataset
    X_train, X_rem,T_train, T_rem = split_data(X, T, train_percentage=0.8)

    # Now since we want the valid and test size to be equal (10% each of overall data). 
    # we have to define valid_size=0.5 (that is 50% of remaining data)
    X_val, X_test, T_val, T_test = train_test_split(X_rem,T_rem, test_size=0.5)
    
    best_db_model = model_repository.find_best_model(lang_name)
    best_sh_model = from_db_model_to_sh_model(best_db_model, lang_name)
    
    # compute current accuracy of model on validation set
    cur_acc = compute_accuracy(best_sh_model, X_val, T_val)
    
    # train model on training set
    train(best_sh_model, X_train, T_train)
    
    # compute accuracy of model on test set
    new_acc = compute_accuracy(best_sh_model, X_test, T_test)

    print(f"new_acc = {new_acc} and cur_acc = {cur_acc}, ", flush=True)
    if new_acc > cur_acc:
        print("[SHModel] Persisting model to directory ", flush=True)
        best_sh_model.persist_model()
        improved_db_model = from_best_sh_model_to_db_model(lang_name, new_acc)
        model_repository.save(improved_db_model)
        annotation_repository.update_trained_time(training_data)
        return

    print("[TRAIN] No improvement: do nothing", flush=True)


"""
fnc which trains the model based on a number on epochs. 
Before the start of the training process, the model will be set into the finetuning mode.
Training data will be shuffled before the start of the process.
Function returns np array with losses
"""
def train(model, X_train, T_train, epochs=10):
    model.setup_for_finetuning()
    X_train, T_train = shuffle_data(X_train, T_train)
    losses = np.array([])
    for epoch in range(epochs):
        print(f'Loading {epoch+1/10}%', flush=True)
        epoch_losses = np.array([])
        for idx, x in enumerate(X_train):
            loss_of_sample = model.finetune_on(x, T_train[idx])
            epoch_losses = np.append(epoch_losses, loss_of_sample)
        avg_epoch_loss = np.mean(epoch_losses)
        losses = np.append(losses, avg_epoch_loss)
        print(f'Average Loss {avg_epoch_loss} in epoch {epoch+1}', flush=True)
    return losses

"""
fnc which takes two np arrays and shuffles them accordingly
returns two shuffled np arrays 
"""
def shuffle_data(X, T):
    print("[TRAIN] shuffling data...", flush=True)
    assert len(X) == len(T)
    X, T = shuffle(X, T, random_state=0)
    return X, T

"""
fnc which takes two np arrays as paramets and splits the two arrays into training and validation data
Returns 4 np arrays with default split of 0.8 training & 0.2 validation data 
"""
def split_data(X, T, train_percentage=0.8):
    print("[TRAIN] splitting data...", flush=True)
    X_train, X_val,T_train, T_val = train_test_split(X,
                                                     T, 
                                                     train_size=train_percentage, 
                                                     random_state=42,
                                                    shuffle=False)
    
    assert X_train.shape == T_train.shape
    assert X_val.shape == T_val.shape

    return X_train, X_val,T_train, T_val

"""
fnc which takes a SHModel with two np arrays as input.
the SHModel predicts based on the lexing tokens in the X arrays a highlighting token
The output of the predict function will be compared to the highlighting token in the T array.
If predicted highlighting token equals the highlighting token of the T array the var correct is incremented
In any case the var total will be incremented. 
Returns a value between 0 & 1 due to the divison of correct/total
"""
def compute_accuracy(model, X, T):
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
