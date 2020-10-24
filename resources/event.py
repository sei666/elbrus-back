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
        event = Event(**body, author = authUser, autorFIO = authUser.fio)
        event.save()
        refurl = RefUrl(event = event.id)
        refurl.save()
        refurl.hash_url(refurl.id)
        refurl.save()     
##--------------------------------------------------------------------------------------------------------------------------------------
