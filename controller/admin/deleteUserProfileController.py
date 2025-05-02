from entity.UserProfile import UserProfile

class DeleteProfileController:
    @staticmethod
    def delete_profile(profile_id):
        """
        Delete a user profile
        
        Args:
            profile_id: The unique identifier for the profile
            
        Returns:
            tuple: (success_bool, message_str)
        """
        try:
            # Find the profile
            profile = UserProfile.find_by_profile_id(profile_id)
            
            if not profile:
                return False, "Profile not found"
            
            # Delete the profile using entity method
            profile.delete_from_db()
            
            return True, "Profile deleted successfully"
            
        except Exception as e:
            return False, f"Error deleting profile: {str(e)}"