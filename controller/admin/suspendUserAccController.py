from entity.UserAccount import User
from db_config import db

class SuspendUserAccController:
    @staticmethod
    def suspend_user(user_id):
        """
        Suspend a user by setting isActive to False
        """
        try:
            # Find user by ID
            user = User.find_by_id(user_id)
            
            if not user:
                return False, "User not found"
            
            # Set isActive to False (suspended)
            user.suspend()
            return True, "User suspended successfully"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error suspending user: {str(e)}"
    
