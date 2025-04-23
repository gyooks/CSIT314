from entity.UserAccount import User
from db_config import db

class viewUserAccController:
    @staticmethod
    def get_all_users():
        """
        Get all users from database
        """
        try:
            users = User.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            return []
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        """
        try:
            user = User.query.get(user_id)
            if user:
                user_dict = user.to_dict()
                if user.profile:
                    user_dict['profile'] = user.profile.to_dict()
                return user_dict
            return None
        except Exception as e:
            return None