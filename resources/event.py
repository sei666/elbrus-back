#~elbrus-back/resources/post.py
import json
import requests


from posixpath import join
from app import app

import datetime

import socket
# from app import storage


from flask import Response, request, jsonify

from database.models import Event, User, RefUrl
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from flask_restful import Resource

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from resources.errors import SchemaValidationError, EventAlreadyExistsError, \
InternalServerError, UpdatingEventError, DeletingEventError, EventNotExistsError


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

