from entity.UserProfile import UserProfile

class UpdateProfileController:
    @staticmethod
    def get_profile_by_profile_id(role_id):
        """Get a user profile/role by ID for updating"""
        return UserProfile.find_by_id(role_id)
    
    @staticmethod
    def update_profile(role_id, role_name, description):
        """Update a user profile/role"""
        
        # Find profile
        profile = UserProfile.find_by_id(role_id)
        if not profile:
            return False, "User role not found"
        
        # Check if new name already exists (and it's not this profile)
        existing_profile = UserProfile.find_by_name(role_name)
        if existing_profile and existing_profile.role_id != role_id:
            return False, "A user role with this name already exists"
        
        # Update profile
        try:
            profile.update_in_db(role_name=role_name, description=description)
            return True, "User role updated successfully"
        except Exception as e:
            return False, f"Error updating user role: {str(e)}"