from entity.UserProfile import UserProfile

class CreateUserProfileController:
    @staticmethod
    def create_profile(role_name, description=None):
        """Create a new user profile/role"""
        
        # Check if profile with same name already exists
        existing_profile = UserProfile.find_by_name(role_name)
        if existing_profile:
            return False, "A user role with this name already exists"
        
        # Create new profile
        try:
            new_profile = UserProfile(role_name=role_name, description=description)
            new_profile.save_to_db()
            return True, "User role created successfully"
        except Exception as e:
            return False, f"Error creating user role: {str(e)}"