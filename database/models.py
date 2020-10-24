#~elbrus-back/database/models.py
import datetime
from bson.objectid import ObjectId

from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import hashlib
import mongoengine_goodjson as gj

salt_hash = "GurgenMishaSosik"

class RefUrl(gj.Document):
    url = db.StringField(unique=True)
    event = db.ReferenceField('Event')
    def hash_url(self, eventId):
        hash_object = hashlib.sha1((eventId + salt_hash).encode())
        hex_dig = hash_object.hexdigest()
        self.url = hex_dig

class Event(gj.Document):
    typeEntity = db.StringField(required=True, default = "Event")
    typeEvent = db.StringField(required=True, default = "Online")
    author = db.ReferenceField('User')
    autorFIO = db.StringField(required=True, "")
    managerFIO = db.StringField(required=True, "")
    description = db.StringField(required=True, "")
    registrationCount = db.IntField(required = True, default = 0)
    testingCount = db.IntField(required = True, default = 0)
    registrationListCounter = db.ListField(db.ReferenceField('User'))
    refUrl = db.StringField(required=True, "")
    timeStart = db.DateTimeField()

class User(gj.Document):
    typeEntity = db.StringField(required=True, default = "User")
    username = db.StringField(required=True, unique=True, min_length=3)
    fio = db.StringField(required=True, unique=True, min_length=3)
    email = db.EmailField(required=True, unique=True, exclude_json=True)
    password = db.StringField(required=True, min_length=6, exclude_json=True)
    eventsCounter = db.IntField(required=True, default = 0)
    typeProfile = db.StringField(required=True, default = "Base")
    eventsCreatedList = db.ListField(db.ReferenceField('Event'))
    refLinkCounts = db.IntField(required=True, default = 0)
    eventsAttendedList = db.ListField(db.ReferenceField('Event'))
    created = db.DateTimeField(default=datetime.datetime.utcnow, exclude_json=True)  
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
