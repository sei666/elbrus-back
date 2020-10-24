#~elbrus-back/database/models.py
import datetime
from bson.objectid import ObjectId

from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import hashlib
import mongoengine_goodjson as gj

salt_hash = "ElbrusHackathon"

class RefUrl(gj.Document):
    url = db.StringField(unique=True)
    event = db.ReferenceField('Event')
    def hash_url(self, urlId):
        hash_object = hashlib.sha1((urlId + salt_hash).encode())
        hex_dig = hash_object.hexdigest()
        self.url = hex_dig

class Event(gj.Document):
    typeEntity = db.StringField(required=True, default = "Event")
    typeEvent = db.StringField(required=True, default = "Online")
    author = db.ReferenceField('User')
    authorFIO = db.StringField(required=True, default = "")
    managerFIO = db.StringField(required=True, default = "")
    description = db.StringField(required=True, default = "")
    registrationCount = db.IntField(required = True, default = 0)
    testingCount = db.IntField(required = True, default = 0)
    registrationList = db.ListField(db.ReferenceField('User'))
    refUrl = db.StringField(required=True,  default = "")
    urlForTelegram = db.StringField(required=True,  default = "")
    refUrlRegistrationCount = db.IntField(required = True, default = 0)
    timeStart = db.DateTimeField()
    rating = db.IntField(required = True, default = 0)
    numberOfRated = db.IntField(required = True, default = 0)
    ratingList = db.ListField(db.ReferenceField('User'), exclude_json=True)
    statusEvent = db.StringField(required=True,  default = "Actual")
    flyerPassCount = db.IntField(required = True, default = 0)
    flyerPassList = db.ListField(db.ReferenceField('User'), exclude_json=True)

class User(gj.Document):
    typeEntity = db.StringField(required=True, default = "User")
    username = db.StringField(required=True, unique=True, min_length=3)
    fio = db.StringField(required=True, unique=True, min_length=3)
    email = db.EmailField(required=True, unique=True, exclude_json=True)
    password = db.StringField(required=True, min_length=6, exclude_json=True)
    eventsCounter = db.IntField(required=True, default = 0)
    typeProfile = db.StringField(required=True, default = "Base")
    eventsCreatedList = db.ListField(db.ReferenceField('Event'))
    bonuses = db.IntField(required=True, default = 0)
    refLinkCounts = db.IntField(required=True, default = 0)
    eventsAttendedList = db.ListField(db.ReferenceField('Event'))
    created = db.DateTimeField(default=datetime.datetime.utcnow, exclude_json=True)  
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
