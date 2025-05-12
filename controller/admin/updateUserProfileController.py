from entity.UserProfile import UserProfile

class UpdateProfileController:
    @staticmethod
    def update_profile(role_id, role_name=None, description=None):
        """
        Get profile and update information if data is provided
        """
        # Find profile
        profile = UserProfile.find_by_id(role_id)
        if not profile:
            return False, "User role not found", None
            
        # If no update data is provided, just return the profile (for GET requests)
        if role_name is None and description is None:
            return True, "Profile retrieved", profile
        
        # Check if new name already exists (and it's not this profile)
        if role_name:
            existing_profile = UserProfile.find_by_name(role_name)
            if existing_profile and existing_profile.role_id != role_id:
                return False, "A user role with this name already exists", profile
            
        # Update profile
        try:
            profile.update_in_db(role_name=role_name, description=description)
            return True, "User role updated successfully", profile
        except Exception as e:
            return False, f"Error updating user role: {str(e)}", profile