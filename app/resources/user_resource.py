from flask_restful import Resource
from flask import request
from db import db
from pydantic import ValidationError
from app.schemas.user_schema import UserSchema
from app.models.user_model import User
from app.utils.helpers import hash_password
from app.services.user_service import user_service
from app.schemas.show_user_schema import ShowAllUserInformation
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserResource(Resource):
    def get(self):
        try:
            users: list[User] = User.query.all()
            users_list = [user.to_json() for user in users]
            return users_list, 200
        except Exception as e:
            
            return {
                'error': str(e)
            }, 400
    
    def post(self):
        try:
            data = request.get_json()
            validated_data = UserSchema.model_validate(data)

            created_user = User(
                name=validated_data.name,
                last_name=validated_data.last_name,
                email=validated_data.email,
                password=hash_password(validated_data.password)
            )

            db.session.add(created_user)
            db.session.commit()
            
            return created_user.to_json(), 201
        
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400

class ManageUserResource(Resource):
    @jwt_required()
    def get(self, user_id: int):
        try:
            current_user_id = get_jwt_identity()
            if int(current_user_id) != user_id:
                return {
                    'error': 'You are not authorized!'
                }, 403
            
            user = user_service.get_by_id(user_id)
            if not user:
                return {
                    'error': 'User was not found'
                }, 404
            
            result = ShowAllUserInformation.model_validate(user)
            return result.model_dump(mode='json'), 200
        
        except Exception as e:
            return {
                'error': str(e)
            }, 404
        
    @jwt_required()
    def put(self, user_id: int):
        try:
            current_user_id = get_jwt_identity()
            if int(current_user_id) != user_id:
                return {
                    'error': 'You are not authorized'
                }, 403
            
            user = user_service.get_by_id(user_id)

            if not user:
                return {
                    'error': 'User was not found'
                }, 404
            
            data = request.get_json()
            validated_data = UserSchema.model_validate(data)

            user.name = validated_data.name
            user.last_name = validated_data.last_name
            user.email = validated_data.email

            db.session.commit()
            return user.to_json(), 200
        
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 404

    @jwt_required() 
    def delete(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            if int(current_user_id) != user_id:
                return {
                    'error':'You are not authorized'
                }, 403
            
            user = user_service.get_by_id(user_id)

            if not user:
                return {
                    'error': 'User was not found'
                }, 404
            
            user.is_active = False
            
            db.session.commit()

            return {
                'message': 'User deleted successfully'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400