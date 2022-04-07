import logging
from model.SHModelUtils import SHModel
from flask import Flask, Response, request, jsonify
from flask_mongoengine import MongoEngine
from sklearn.utils import shuffle
import numpy as np
import os

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
    logging.info('[TRAIN] training started')

    supported_languages = ["java", "python3", "kotlin"]
    for language in supported_languages:
        training_batch = Annotation.objects(language=language)
        logging.info('[TRAIN] data loaded')

        # TODO. data preprocessing
        improve_model(X, T)


    # TODO: ?? DEV BRANCH??
    # TODO: ?? objects(batch==None), fetch only not already trained (db attribute)
    # TODO: ?? where does the duplication check takes place? (primary key is id, why not lexing? or tokIds probably?)
    annotation_batch = Annotation.objects()
    logging.info('[TRAIN] data loaded')
    # TODO: split data

    # TODO: ?? train and validate model (extract tokenIds and hValues)
    # TODO: load existing model and compare accuracy
    # TODO: store new model on DB if validation is better
    return jsonify([annotation.to_json() for annotation in annotation_batch])

def improve_model(X, T):
    X_train, T_train, X_val, T_val = split_data(X, T)
    X_train, T_train = shuffle_data(X_train, T_train)
    train(X_train, T_train)
    new_acc = accuracy(X_val, T_val)
    print(new_acc)

    # curr_acc = accuracy(X_val, T_val)

    if new_acc > curr_acc:
        return True

def train(X, T, model, epochs=10):
    model.setup_for_finetuning()
    losses = np.array([])
    for epoch in range(epochs):
        print(f'Loading {epoch+1}0%')
        epoch_losses = np.array([])
        for idx, x in enumerate(X):
            epoch_loss = model.finetune_on(x, T[idx])
            epoch_losses = np.append(epoch_losses, epoch_loss)
        avg_epoch_loss = np.mean(epoch_losses)
        losses = np.append(losses, avg_epoch_loss)
        print(f'Average Loss {avg_epoch_loss} in epoch {epoch+1}')
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


"""

def get_db():
    client = MongoClient(host=os.environ.get('MONGODB_HOST', 'localhost'),
                         port=int(os.environ.get('MONGO_PORT')),
                         username=os.environ.get('MONGO_USERNAME'),
                         password=os.environ.get('MONGO_PASSWORD'),
                         authSource=os.environ.get('MONGO_AUTH_DATABASE'))
    db = client[os.environ.get('MONGO_DATABASE_NAME')]
    return db

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/animals')
def get_stored_animals():
    db = get_db()
    res = db.palma.find()
    return Response(json.dumps({'h_code_values': res}))



app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('MONGO_DATABASE_NAME'),
    'host': os.environ.get('MONGO_HOST'),
    'port': int(os.environ.get('MONGO_PORT'))
}
db = MongoEngine()
db.init_app(app)

class Palma(db.Document):
    sourceCode = db.StringField()
    lexingTokes = db.StringField()
    highlightingTokens = db.StringField()
    highlightingCode = db.StringField()

@app.route("/train", methods=["GET"])
def train():
    logging.info("train")
    print(Palma.objects().first())
    print(Palma.objects(sourceCode="public static void main(String[] args) {} ").first())

    return Response(status=200)


    supported_languages = ["java", "python3", "kotlin"]
    logging.info('Python HTTP trigger function processed a request.')

    # deserialize
    try:
        req_body = request.get_json()
        lang_name = req_body.get('lang_name')
        tok_ids = req_body.get('tok_ids')
    except Exception as e:
        logging.error("Invalid body, not json" + str(e))
        return Response("Invalid body, please provide json", status=400)

    # handle unsupported languages
    if lang_name not in supported_languages:
        logging.error("Unsupported language")
        return Response(f"{lang_name} is an unsupported programming language", status=400)

    try:    
        # predict
        model = SHModel(lang_name, "curr")
        model.setup_for_prediction()
        res = model.predict(tok_ids)
        return Response(json.dumps({'h_code_values': res}))
    except Exception as e:
        logging.error("Model error: " + str(e))
        return Response("Model error: " + str(e), status=500)

"""
    

if __name__ == "__main__":
    app.run(debug=True)
