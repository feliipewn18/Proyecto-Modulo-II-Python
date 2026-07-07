from app.models.user_model import User
from typing import Union

class UserService:
    def find_by_email(self, email: str) -> User | None:
        user = User.query.filter_by(email=email).first()
        return user
    def get_by_id(self, user_id: int) -> Union[User, None]:
        user = User.query.get(user_id)
        return user
    
user_service = UserService()