from flask_restful import Resource
from flask import request
from db import db
from pydantic import ValidationError
from app.models.task_model import Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.task_schema import TaskSchema

class TaskResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            tasks = Task.query.filter_by(user_id=user_id).all()
            return [task.to_json() for task in tasks], 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400
    
    @jwt_required()
    def post(self):
        try:
            user_id = int(get_jwt_identity())
            data = request.get_json()
            validated_data = TaskSchema.model_validate(data)
            new_task = Task(
                title=validated_data.title,
                description=validated_data.description,
                priority=validated_data.priority,
                due_date=validated_data.due_date,
                user_id=user_id             
            )
            
            db.session.add(new_task)
            db.session.commit()

            return new_task.to_json(), 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400
        
class ManageTasksResource(Resource):
    @jwt_required()
    def get(self, task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()

            if not task:
                return {
                    'error': 'Task was not found'
                }, 404
            return task.to_json(), 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 404
    
    @jwt_required()
    def put(self, task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()

            if not task:
                return {
                    'error': 'Task was not found'
                }, 404
            
            data = request.get_json()
            validated_data = TaskSchema.model_validate(data)
            
            task.title = validated_data.title
            task.description = validated_data.description
            task.priority = validated_data.priority
            task.due_date = validated_data.due_date

            db.session.commit()
            
            return task.to_json(), 200
        
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
    def delete(self, task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()

            if not task:
                return {
                    'error': 'Task was not found'
                }, 404
            db.session.delete(task)
            db.session.commit()

            return {
                'message': 'Task was successfully deleted'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400
        
class TaskCompleteResource(Resource):
    @jwt_required()
    def patch(self, task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            
            if not task:
                return {
                    'error': 'Task was not found'
                }, 404
            
            task.is_completed = not task.is_completed
            db.session.commit()

            return task.to_json(), 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400