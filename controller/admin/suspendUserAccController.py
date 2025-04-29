from entity.UserAccount import User
from db_config import db

class suspendUserAccController:
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
    
    @staticmethod
    def reactivate_user(user_id):
        """
        Reactivate a suspended user by setting isActive to True
        """
        try:
            # Find user by ID
            user = User.find_by_id(user_id)
            
            if not user:
                return False, "User not found"
            
            # Set isActive to True (reactivated)
            user.reactivate()
            return True, "User reactivated successfully"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error reactivating user: {str(e)}"