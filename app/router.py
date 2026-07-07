from flask_restful import Api
from app import app
from app.resources.auth_resource import *
from app.resources.user_resource import *
from app.resources.task_resource import *

api = Api(app, prefix='/api/v1')

api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

api.add_resource(UserResource, '/users')
api.add_resource(ManageUserResource, '/users/<int:user_id>')

api.add_resource(TaskResource, '/tasks')
api.add_resource(ManageTasksResource, '/tasks/<int:task_id>')
api.add_resource(TaskCompleteResource, '/tasks/<int:task_id>/complete')