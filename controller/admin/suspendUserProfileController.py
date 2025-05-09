from entity.UserProfile import UserProfile

class SuspendProfileController:
    @staticmethod
    def suspend_profile(role_id):
        """Suspend a user profile/role"""
        
        profile = UserProfile.find_by_id(role_id)
        if not profile:
            return False, "User role not found"
        
        try:
            profile.suspend()
            return True, f"User role '{profile.role_name}' has been suspended"
        except Exception as e:
            return False, f"Error suspending user role: {str(e)}"
    
    @staticmethod
    def reactivate_profile(role_id):
        """Reactivate a suspended user profile/role"""
        
        profile = UserProfile.find_by_id(role_id)
        if not profile:
            return False, "User role not found"
        
        try:
            profile.reactivate()
            return True, f"User role '{profile.role_name}' has been reactivated"
        except Exception as e:
            return False, f"Error reactivating user role: {str(e)}"

