from entity.UserAccount import User
from db_config import db

class viewUserAccController:
    @staticmethod
    def get_all_users():
        """
        Get all users from database
        """
        try:
            users = User.get_all()
            return [user.to_dict() for user in users]
        except Exception as e:
            return []
    
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
    
    @staticmethod
    def update_user(user_id, email, phone, role, is_active):
        """
        Update user attributes
        """
        try:
            user = User.find_by_id(user_id)
            if not user:
                return False

            user.update_in_db(email, phone, role, is_active)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            db.session.rollback()
            return False