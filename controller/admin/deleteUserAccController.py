from entity.UserAccount import User
from db_config import db

class deleteUserAccController:   

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        """
        try:
            user = User.find_by_id(user_id)
            if user:
                user_dict = user.to_dict()
                if user.profile:
                    user_dict['profile'] = user.profile.to_dict()
                return user_dict
            return None
        except Exception as e:
            return None
        
    @staticmethod
    def delete_user(user_id):
        user = User.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return True
        return False
    