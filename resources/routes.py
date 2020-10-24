#~elbrus-back/resources/routes.py

#from .movie import MoviesApi, MovieApi
from .event import EventAddApi
from .auth import SignupApi, LoginApi, CheckUniqUser, CheckUniqEmail, GetUser, GetUserByToken
from .reset_password import ForgotPassword, ResetPassword

def initialize_routes(api):
 api.add_resource(EventAddApi, '/api/event/eventAddApi')

 api.add_resource(SignupApi, '/api/auth/signup')
 api.add_resource(LoginApi, '/api/auth/login')
 api.add_resource(CheckUniqUser,'/api/auth/checkUniqUser/<name>')
 api.add_resource(CheckUniqEmail,'/api/auth/checkUniqEmail/<email>')
 api.add_resource(GetUserByToken,'/api/auth/getUserByToken')

 api.add_resource(ForgotPassword, '/api/auth/forgot')
 api.add_resource(ResetPassword, '/api/auth/reset')