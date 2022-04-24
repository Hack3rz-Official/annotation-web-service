import numpy as np
import os
from sklearn.utils import shuffle
from src.repositories.annotation import AnnotationRepository
from src.repositories.model import ModelRepository
import config as config
from src.util.SHModelHelper import from_db_model_to_sh_model, from_best_sh_model_to_db_model

annotation_repository = AnnotationRepository()
model_repository = ModelRepository()

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
        improve_model(X, T, lang_name)
        trained_languages.append(lang_name)

    print("[TRAIN] ### TRAINING DONE ### ", flush=True)

    if not trained_languages:
        return "No languages trained. Not enough training data."
    return "Models trained for: " + str(trained_languages)


def data_preprocessing(training_data):
    X = []
    T = []
    for sample in training_data:
        X.append(sample.lexingTokens)
        T.append(sample.highlightingTokens)
    X = np.array(X, dtype=object)
    T = np.array(T, dtype=object)
    return X, T


def improve_model(X, T, lang_name):
    X_train, T_train, X_val, T_val = split_data(X, T)

    best_db_model = model_repository.find_best_model(lang_name)
    best_sh_model = from_db_model_to_sh_model(best_db_model, lang_name)
    
    cur_acc = compute_accuracy(best_sh_model, X_val, T_val)
    train(best_sh_model, X_train, T_train)
    new_acc = compute_accuracy(best_sh_model, X_val, T_val)

    print(f"new_acc = {new_acc} and cur_acc = {cur_acc}, ", flush=True)
    if new_acc > cur_acc:
        print("[SHModel] Persisting model to directory ", flush=True)
        best_sh_model.persist_model()
        improved_db_model = from_best_sh_model_to_db_model(lang_name, new_acc)
        model_repository.save(improved_db_model)
        return

    print("[TRAIN] No improvement: do nothing", flush=True)


def train(model, X_train, T_train, epochs=10):
    model.setup_for_finetuning()
    X_train, T_train = shuffle_data(X_train, T_train)
    losses = np.array([])
    for epoch in range(epochs):
        print(f'Loading {epoch+1}0%', flush=True)
        epoch_losses = np.array([])
        for idx, x in enumerate(X_train):
            epoch_loss = model.finetune_on(x, T_train[idx])
            epoch_losses = np.append(epoch_losses, epoch_loss)
        avg_epoch_loss = np.mean(epoch_losses)
        losses = np.append(losses, avg_epoch_loss)
        print(f'Average Loss {avg_epoch_loss} in epoch {epoch+1}', flush=True)
    return losses


def shuffle_data(X, T):
    print("[TRAIN] shuffling data...", flush=True)
    assert len(X) == len(T)
    shuffle(X, T, random_state=0)
    return X, T


def split_data(X, T, train_percentage=0.8):
    print("[TRAIN] splitting data...", flush=True)
    N = X.shape[0]
    train_size = int(train_percentage * N)

    X_train = X[:train_size]
    T_train = T[:train_size]
    X_val = X[train_size:]
    T_val = T[train_size:]

    assert X_train.shape[0] == T_train.shape[0]
    assert X_val.shape[0] == T_val.shape[0]

    return X_train, T_train, X_val, T_val


def compute_accuracy(model, X, T):
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
