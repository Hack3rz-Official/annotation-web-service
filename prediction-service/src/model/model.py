from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Model(db.Document):
    file = db.FileField()
    supported_languages = ('JAVA', 'PYTHON3', 'KOTLIN')
    language = db.StringField(required=True, choices=supported_languages)
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