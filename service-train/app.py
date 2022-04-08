import logging
from model.SHModelUtils import SHModel
from flask import Flask, Response, request, jsonify
from flask_mongoengine import MongoEngine
from sklearn.utils import shuffle
import numpy as np
import os
import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('MONGO_DATABASE_NAME'),
    'host': os.environ.get('MONGO_HOST', 'localhost'),
    'port': int(os.environ.get('MONGO_PORT')),
    'username': os.environ.get('MONGO_USERNAME'),
    'password': os.environ.get('MONGO_PASSWORD'),
    'authSource': os.environ.get('MONGO_AUTH_DATABASE')
}
db = MongoEngine()
db.init_app(app)

MODEL_NAME = "cur"

class Model(db.Document):
    file = db.FileField()
    language = db.StringField()
    createdTime = db.DateTimeField(default=datetime.datetime.now())
    meta = {
        'collection': 'models',
        'strict': False
    }

class Annotation(db.Document):
    sourceCode = db.StringField()
    lexingTokes = db.ListField()
    highlightingTokens = db.ListField()
    highlightingCode = db.StringField()
    language = db.StringField()
    meta = {
        'collection': 'annotations',
        'strict': False
    }

    def to_json(self):
        return {
            "sourceCode": self.sourceCode,
            "lexingTokes": self.lexingTokes,
            "highlightingTokens": self.highlightingTokens,
            "highlightingCode": self.highlightingCode,
            "language": self.language
        }

@app.route('/train', methods=['GET'])
def train():    
    print("[TRAIN] ### TRAINING STARTED ### ", flush=True)

    supported_languages = ["java"]
    for lang_name in supported_languages:
        print("[TRAIN] Starting model training for " + lang_name, flush=True)

        training_data = Annotation.objects(language=lang_name.upper())
        print("[TRAIN] Training data loaded from DB: " + str(len(training_data)), flush=True)

        if len(training_data) < int(os.environ.get('TRAINING_BATCH_SIZE')):
            print("[TRAIN] Not enough data to train model", flush=True)
            continue
        
        # data preprocessing
        X = []
        T = []
        for sample in training_data:
            X.append(sample.lexingTokes)
            T.append(sample.highlightingTokens)
        X = np.array(X, dtype=object)
        T = np.array(T, dtype=object)

        improve_model(X, T, lang_name)

    print("[TRAIN] ### TRAINING DONE ### ", flush=True)
    return Response(status=200)


def load_cur_model_from_db(lang_name):
    cur_model = Model.objects(language=lang_name).order_by('-createdTime').first()
    if cur_model:
        print(f"[SHModel] Newest Model loaded from DB with createdTime {cur_model.createdTime}", flush=True)
        with open(lang_name + "_" + MODEL_NAME + ".pt", "wb") as file:
            cur_model_file = cur_model.file.read()
            file.write(cur_model_file)
    else:
        print("[SHModel] No model found in DB, creating new model", flush=True)

    return SHModel(lang_name, MODEL_NAME)

def save_model_to_db(lang_name):
    print("[TRAIN] New Model saved from directory to DB ", flush=True)
    model = Model(language=lang_name)
    with open(lang_name + "_" + MODEL_NAME + ".pt", "rb") as binary_file:
        model.file.put(binary_file)
        
    model.save()

def improve_model(X, T, lang_name):
    X_train, T_train, X_val, T_val = split_data(X, T)

    cur_model = load_cur_model_from_db(lang_name)
    cur_acc = accuracy(cur_model, X_val, T_val)
    train(cur_model, X_train, T_train)
    new_acc = accuracy(cur_model, X_val, T_val)

    print(f"new_acc = {new_acc} and cur_acc = {cur_acc}, ", flush=True)
    if new_acc > cur_acc:
        print("[SHModel] Persisting model to directory ", flush=True)
        cur_model.persist_model()
        save_model_to_db(lang_name)
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

def accuracy(model, X, T):
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

if __name__ == "__main__":
    app.run(debug=True)
