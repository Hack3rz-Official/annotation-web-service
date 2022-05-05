from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()


class Model(db.Document):
    #Representation of an SHModel on the db with all the necessary information about a model
    file = db.FileField()
    language = db.StringField()
    createdTime = db.DateTimeField()
    accuracy = db.FloatField()
    meta = {
        'collection': 'models',
        'strict': False
    }

    def save(self, *args, **kwargs):
        #Populates the field createdTime when triggert on an object of class Model
        if not self.createdTime:
            self.createdTime = datetime.datetime.now()
        return super(Model, self).save(*args, **kwargs)