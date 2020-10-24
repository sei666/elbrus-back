#~elbrus-back/resources/routes.py

from .event import EventAddApi, EventsGetApi, EventRegistrationApi, EventGetByIdApi, EventGetByHashApi,RatingTheEventApi, FlyerGeneratorApi, FlyerCheckApi
from .auth import SignupApi, LoginApi, CheckUniqUser, CheckUniqEmail, GetUser, GetUserByToken
from .reset_password import ForgotPassword, ResetPassword

def initialize_routes(api):
 api.add_resource(EventGetByIdApi, '/api/event/eventGetByIdApi/<eventId>')
 api.add_resource(EventGetByHashApi, '/api/event/eventGetByHashApi/<hashUrl>')
 api.add_resource(EventAddApi, '/api/event/eventAddApi')
 api.add_resource(EventsGetApi, '/api/event/eventsGetApi/<lastEventId>')
 api.add_resource(EventRegistrationApi,'/api/event/eventRegistration')

 api.add_resource(RatingTheEventApi, '/api/event/ratingTheEventApi')

 api.add_resource(FlyerGeneratorApi, '/api/event/flyerGeneratorApi')
 api.add_resource(FlyerCheckApi, '/api/event/flyerCheckApi/<bigHash>')

 api.add_resource(SignupApi, '/api/auth/signup')
 api.add_resource(LoginApi, '/api/auth/login')
 api.add_resource(CheckUniqUser,'/api/auth/checkUniqUser/<name>')
 api.add_resource(CheckUniqEmail,'/api/auth/checkUniqEmail/<email>')
 api.add_resource(GetUserByToken,'/api/auth/getUserByToken')

 api.add_resource(ForgotPassword, '/api/auth/forgot')
 api.add_resource(ResetPassword, '/api/auth/reset')