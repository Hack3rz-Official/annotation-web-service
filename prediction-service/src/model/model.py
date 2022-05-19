from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()


class Model(db.Document):
    """
    The Model database document that is used to store and retrieve the model from the database.
    """

    file = db.FileField()
    "A GridFS like file object that supports common methods such as .read(), .readline() and .seek()"

    supported_languages = ('JAVA', 'PYTHON3', 'KOTLIN')
    language = db.StringField(required=True, choices=supported_languages)
    createdTime = db.DateTimeField()
    accuracy = db.FloatField()
    trainingDataAmount = db.IntField()
    validationDataAmount = db.IntField()
    meta = {
        'collection': 'models',
        'strict': False
    }

    def save(self, *args, **kwargs):
        if not self.createdTime:
            self.createdTime = datetime.datetime.now()
        return super(Model, self).save(*args, **kwargs)