from entity.UserProfile import UserProfile

class createUserProfileController:
    @staticmethod
    def create_profile(user_id, first_name, last_name, address=None, phone=None):
        """
        Create a new user profile for an existing user account
        
        Returns:
            tuple: (success_bool, message_str)
        """
        try:
            # Validate required fields
            if not first_name or not last_name:
                return False, "First name and last name are required"
                
            # Create user profile
            user_profile = UserProfile(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone
            )
            
            # Save to db through entity
            user_profile.save_to_db()
            
            return True, "User profile created successfully"
                
        except Exception as e:
            return False, f"Error creating user profile: {str(e)}"