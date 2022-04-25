from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Model(db.Document):
    file = db.FileField()
    language = db.StringField()
    createdTime = db.DateTimeField(default=datetime.datetime.now().astimezone())
    accuracy = db.FloatField()
    meta = {
        'collection': 'models',
        'strict': False
    }
