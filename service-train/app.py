import logging
from model.SHModelUtils import SHModel
from flask import Flask, Response, request, jsonify
from flask_mongoengine import MongoEngine
from sklearn.utils import shuffle
import numpy as np
import os
import pickle
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
    print("Hello? Anyone there?", flush=True)
    
    supported_languages = ["java"]
    for lang_name in supported_languages:
        X = np.array([])
        T = np.array([])

        """
        if len(training_batch) < os.environ.get('TRAINING_BATCH_SIZE'):
            continue
        """

        annotations = Annotation.objects(language=lang_name.upper())
        for sample in annotations:
            X = np.append(X, sample.lexingTokes)
            T = np.append(T, sample.highlightingTokens)

        improve_model(X, T, lang_name)

    return Response(status=200)


def load_cur_model_from_db(lang_name):
    cur_model = Model.objects(language=lang_name).order_by('createdTime').first()
    if cur_model:
        print(cur_model.createdTime, flush=True)
        model_name = "cur"
        with open(lang_name + "_" + model_name +".pt", "wb") as file:
            cur_model_file = cur_model.file.read()
            file.write(cur_model_file)

    return SHModel(lang_name, model_name)

def save_model_to_db(lang_name):
    model = Model(language=lang_name)
    model_name = "cur"
    with open(lang_name + "_" + model_name + ".pt", "rb") as binary_file:
        model.file.put(binary_file)
        
    model.save()

def improve_model(X, T, lang_name):
    X_train, T_train, X_val, T_val = split_data(X, T)

    cur_model = load_cur_model_from_db(lang_name)
    cur_acc = accuracy(cur_model, X_val, T_val)
    train(X_train, T_train)
    new_acc = accuracy(cur_model, X_val, T_val)

    if new_acc > cur_acc:
        cur_model.persist_model()
        print('stored new model to db', flush=True)
        save_model_to_db(lang_name)
        return
    
    print('do NOT store new model to db', flush=True)

def train(X_train, T_train, model, epochs=10):
    X_train, T_train = shuffle_data(X_train, T_train)
    model.setup_for_finetuning()
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
    logging.info('[TRAIN] shuffling data...')
    assert len(X) == len(T)
    shuffle(X, T, random_state=0)
    logging.info('[TRAIN] data shhuffled')
    return X, T

def split_data(X, T, train_percentage=0.8):
    logging.info('[TRAIN] splitting data...')
    N = X.shape[0]  
    train_size = int(train_percentage * N) 
    
    X_train = X[:train_size]
    T_train = T[:train_size]
    X_val = X[train_size:]
    T_val = T[train_size:]

    assert X_train.shape[0] == T_train.shape[0]
    assert X_val.shape[0] == T_val.shape[0]

    logging.info('[TRAIN] data splitted')
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
