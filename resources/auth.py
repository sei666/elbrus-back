#~elbrus-back/resources/auth.py
import json
from flask import Response, request, jsonify
from flask_jwt_extended import create_access_token

from database.models import User
from flask_restful import Resource
import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError

class SignupApi(Resource):
  def post(self):
    try:
        body = request.get_json()
        user =  User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200
        
    except FieldDoesNotExist:
        raise SchemaValidationError
    except NotUniqueError:
        raise EmailAlreadyExistsError
    except Exception as e:
        raise InternalServerError


class LoginApi(Resource):
  def post(self):
    try:
        body = request.get_json()
        user = User.objects.get(username=body.get('username'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise UnauthorizedError

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200

    except (UnauthorizedError, DoesNotExist):
        raise UnauthorizedError
    except Exception as e:
        raise InternalServerError


class CheckUniqUser(Resource):
    def get(self,name):
        try:
            user = User.objects.get(username = name)
            return {'uniq': "false"}, 200
        except (DoesNotExist):
            return {'uniq': "true"}, 200

class GetUser(Resource):
    def get(self,name):
        try:
            user = User.objects.get(username = name)
            responseMessage = jsonify(json.loads(user.to_json(epoch_mode=True)))
            return responseMessage
        except (DoesNotExist):
            return None, 200

class CheckUniqEmail(Resource):
    def get(self,email):
        try:
            user = User.objects.get(email = email)
            return {'uniq': "false"}, 200
        except (DoesNotExist):
            return {'uniq': "true"}, 200

class GetUserByToken(Resource):
    @jwt_optional
    def get(self):
        authUserId = get_jwt_identity()
        responseMessage = {"token": "empty"}, 200
        if authUserId:
            user = User.objects.get(id = authUserId)
            responseMessage = jsonify(json.loads(user.to_json(epoch_mode=True)))
        return responseMessage
