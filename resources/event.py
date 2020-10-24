#~elbrus-back/resources/post.py
import json
import requests


from posixpath import join
from app import app

import datetime

import socket
# from app import storage
from cryptography.fernet import Fernet

from flask import Response, request, jsonify

from database.models import Event, User, RefUrl
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from flask_restful import Resource

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from resources.errors import SchemaValidationError, EventAlreadyExistsError, \
InternalServerError, UpdatingEventError, DeletingEventError, EventNotExistsError

keyForFlyer = "_MWygBV7K-rumUcaToDgB6C4hnBAzoG04A2qmSdt_iA="

##--------------------------------------------------------------- Event Add Api ---------------------------------------------------
class EventAddApi(Resource):
    @jwt_required
    def post(self):
        authUserId = get_jwt_identity()
        authUser = User.objects.get(id = authUserId)
        body = request.get_json()
        event = Event(**body, author = authUser, authorFIO = authUser.fio)
        event.save()
        refUrl = RefUrl(event = event.id)
        refUrl.save()
        refUrl.hash_url(str(refUrl.id))
        refUrl.save()
        event.refUrl = refUrl.url
        event.save()
        authUser.update(push__eventsCreatedList = event)
        return {"event.id": str(event.id)}, 200
##--------------------------------------------------------------------------------------------------------------------------------------

##--------------------------------------------------------------- Events Get Api -------------------------------------------------------
class EventsGetApi(Resource):
    def get(self, lastEventId):
        if lastEventId != "0":
            events = Event.objects(id__lt = lastEventId)
        else:
            events = Event.objects()
        eventsJson = json.loads(events.to_json())
        responseMessage = jsonify(eventsJson)
        return responseMessage
##--------------------------------------------------------------------------------------------------------------------------------------

##--------------------------------------------------------------- Event Registration Api --------------------------------------------------
class EventRegistrationApi(Resource):
    @jwt_required
    def post(self):
        authUserId = get_jwt_identity()
        authUser = User.objects.get(id = authUserId)
        body = request.get_json()
        url = body.get('refUrl')
        event = Event.objects.get(id = body.get('eventId'))
        print(authUser.id,event.author.id)
        if authUser.id == event.author.id:
            return {"response": "the author cannot register"}, 200
        for x in event.registrationList:
            if x == authUser:
                return {"response": "already registered"}, 200
        if event.refUrl == url:
            event.refUrlRegistrationCount += 1
            author = event.author
            author.refLinkCounts +=1
            author.save()
        event.registrationCount +=1
        event.save()
        event.update(push__registrationList = authUser)
        return {"response": "registered"}, 200
##-----------------------------------------------------------------------------------------------------------------------------------------

##--------------------------------------------------------------- Event Get By Id Api -----------------------------------------------------
class EventGetByIdApi(Resource):
    def get(self, eventId):
        event = Event.objects.get(id = eventId)
        eventJson = json.loads(event.to_json())
        responseMessage = jsonify(eventJson)
        return responseMessage
##-----------------------------------------------------------------------------------------------------------------------------------------

##--------------------------------------------------------------- Event Get By Hash Api -----------------------------------------------------
class EventGetByHashApi(Resource):
    def get(self, hashUrl):
        refUrl = RefUrl.objects.get(url = hashUrl)
        event = refUrl.event
        eventJson = json.loads(event.to_json())
        responseMessage = jsonify(eventJson)
        return responseMessage
##-----------------------------------------------------------------------------------------------------------------------------------------

##-----------------------------------------------------------------Rating The Event--------------------------------------------------------
class RatingTheEventApi(Resource):
    @jwt_required
    def post(self):
        authUserId = get_jwt_identity()
        authUser = User.objects.get(id = authUserId)
        body = request.get_json()
        event = Event.objects.get(id = body.get('eventId'))
        rate = body.get('rate')
        try:
            rate = int(rate)
            for x in event.registrationList:
                if x.id == authUser.id:
                    for x2 in event.ratingList:
                        if x2.id == authUser.id:
                            return {"response": "already voted"}, 200
                    event.rating += rate
                    event.numberOfRated += 1
                    event.save()
                    event.update(push__ratingList = authUser)
                    return {"response": "vote accepted"}, 200

            return {"response": "no registration"}, 200
        except:
            return {"response": "error value"}, 200
##-----------------------------------------------------------------------------------------------------------------------------------------

##----------------------------------------------------------------Flyer Generator----------------------------------------------------------
class FlyerGeneratorApi(Resource):
    def get(self):
        # cipher_key = Fernet.generate_key()
        cipher = Fernet(keyForFlyer)
        userId = "213123123"
        eventId = "asdasdj"        
        dictionary ={   
        "userId": userId,   
        "eventId": eventId
        }
        json_object = json.dumps(dictionary, indent = 4)

        text = str(json_object).encode()
        encrypted_text = cipher.encrypt(text)
        print(encrypted_text.decode("utf-8"))
        # Дешифруем
        decrypted_text = cipher.decrypt(encrypted_text)
        print(decrypted_text)
        return jsonify(json.loads(decrypted_text))

##----------------------------------------------------------------------------------------------------------------------------------------

##--------------------------------------------------------------Flyer Check Api-----------------------------------------------------------
class FlyerCheckApi(Resource):
    @jwt_optional
    def get(self, bigHash):
        #print(bigHash)
        authUserId = get_jwt_identity()
        if authUserId:
            authUser = User.objects.get(id = authUserId)
        byteHash = bigHash.encode()
        cipher = Fernet(keyForFlyer)
        decrypted_text = cipher.decrypt(byteHash)
        
        #print(decrypted_text)
        #json1 = json.loads(decrypted_text.decode())
        #print(json1)
        #return jsonify(json.loads(json1))



##----------------------------------------------------------------------------------------------------------------------------------------