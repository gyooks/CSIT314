from entity.UserProfile import UserProfile

class UpdateProfileController:
    @staticmethod
    def update_profile(profile_id, first_name, last_name, address, phone):
        """
        Update an existing user profile
        
        Args:
            profile_id: The unique identifier for the profile
            first_name: User's first name
            last_name: User's last name
            address: User's address
            phone: User's phone number
            
        Returns:
            tuple: (success_bool, message_str)
        """
        try:
            # Find the profile
            profile = UserProfile.find_by_profile_id(profile_id)
            
            if not profile:
                return False, "Profile not found"
            
            # Validate required fields
            if not first_name or not last_name:
                return False, "First name and last name are required"
            
            # Update the profile
            profile.update_in_db(
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone
            )
            
            return True, "Profile updated successfully"
            
        except Exception as e:
            return False, f"Error updating profile: {str(e)}"

    @staticmethod
    def get_profile_by_profile_id(profile_id):
        """
        Retrieve a user profile by profile ID
        
        Returns:
            UserProfile or None
        """
        try:
            return UserProfile.find_by_profile_id(profile_id)
        except Exception as e:
            return None