from entity.UserProfile import UserProfile

class ViewUserProfileDetailController:
    
    @staticmethod
    def get_profile_detail(role_id):
        """
        Get detailed information about a specific user profile/role
        
        Args:
            role_id (int): The ID of the user profile/role
            
        Returns:
            UserProfile object or None if not found
        """
        # Retrieve profile by ID from entity layer
        userprofile = UserProfile.find_by_id(role_id)
        
        if userprofile:
            # Get associated users count
            user_count = UserProfile.get_users_count(role_id)
            
            # Add users count to profile object
            userprofile.users_count = user_count
            
        return userprofile