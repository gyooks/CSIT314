from entity.UserAccount import User
from db_config import db

class UpdateUserAccController:
    @staticmethod
    def update_user(user_id, email=None, role_id=None, password=None,
                    first_name=None, last_name=None, address=None, phone=None):
        """
        Get user and update information if data is provided
        """
        try:
            # Find the user
            user = User.find_by_id(user_id)
            if not user:
                return False, "User not found", None
            
            # If no update data is provided, just return the user (for GET requests)
            if all(param is None for param in [email, role_id, password, first_name, last_name, address, phone]):
                return True, "User retrieved", user.to_dict()
            
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
            
            return True, "User updated successfully", user.to_dict()
                
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            print(f"Error with user operation: {error_message}")
            return False, error_message, None