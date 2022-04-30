from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Model(db.Document):
    file = db.FileField()
    language = db.StringField()
    createdTime = db.DateTimeField()
    accuracy = db.FloatField()
    meta = {
        'collection': 'models',
        'strict': False
    }

    def save(self, *args, **kwargs):
        if not self.createdTime:
            self.createdTime = datetime.datetime.now()
        return super(Model, self).save(*args, **kwargs)