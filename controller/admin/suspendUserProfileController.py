from entity.UserProfile import UserProfile

class SuspendProfileController:
    @staticmethod
    def suspend_profile(profile_id):
        """
        Suspend a user profile by setting isActive to False
        
        Returns:
            tuple: (success_bool, message_str)
        """
        try:
            # Find profile by ID
            profile = UserProfile.find_by_profile_id(profile_id)
            
            if not profile:
                return False, "Profile not found"
                
            # Suspend the profile
            profile.suspend()
            
            return True, "Profile suspended successfully"
                
        except Exception as e:
            return False, f"Error suspending profile: {str(e)}"
    
    @staticmethod
    def reactivate_profile(profile_id):
        """
        Reactivate a suspended profile by setting isActive to True
        
        Returns:
            tuple: (success_bool, message_str)
        """
        try:
            # Find profile by ID
            profile = UserProfile.find_by_profile_id(profile_id)
            
            if not profile:
                return False, "Profile not found"
                
            # Reactivate the profile
            profile.reactivate()
            
            return True, "Profile reactivated successfully"
                
        except Exception as e:
            return False, f"Error reactivating profile: {str(e)}"