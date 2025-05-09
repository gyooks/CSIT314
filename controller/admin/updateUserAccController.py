from entity.UserAccount import User
from db_config import db

class UpdateUserAccController:
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID with profile information
        """
        try:
            user = User.find_by_id(user_id)
            if user:
                user_dict = user.to_dict()
                return user_dict
            return None
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    @staticmethod
    def update_user(user_id, email=None, role_id=None, password=None, 
                   first_name=None, last_name=None, address=None, phone=None):
        """
        Update user information
        """
        try:
            # Find the user
            user = User.find_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Update user with all provided information
            user.update_in_db(
                email=email,
                role_id=role_id,
                password=password,  # Will be hashed in the method if not None
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
       
            )
            
            return True, "User updated successfully"
            
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            print(f"Error updating user: {error_message}")
            return False, error_message