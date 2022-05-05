from flask_mongoengine import MongoEngine

db = MongoEngine()


class AnnotationKey(db.EmbeddedDocument):
    language = db.StringField(required=True)
    lexingTokens = db.ListField(required=True)

class Annotation(db.Document):
    key = db.EmbeddedDocumentField(AnnotationKey, primary_key=True)
    sourceCode = db.StringField()
    highlightingTokens = db.ListField()
    highlightingCode = db.StringField()
    trainedTime = db.DateTimeField()
    validatedTime = db.DateTimeField()
    meta = {
        'collection': 'annotations',
        'strict': False
    }
