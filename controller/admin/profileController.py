from entity.UserAccount import User
from entity.UserProfile import UserProfile
from db_config import db

class AdminProfileController:
    def get_admin_profile(self, user_id):
        """Get the profile of the logged-in admin"""
        try:
            # Get user data
            user = User.find_by_id(user_id)
            
            if not user:
                return None
            
            # Check if user has a profile
            profile = UserProfile.find_by_user_id(user_id)
            
            # Prepare result
            result = {
                'userID': user.userID,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
                'first_name': None,
                'last_name': None,
                'address': None
            }
            
            # Add profile data if exists
            if profile:
                result.update({
                    'profile_id': profile.profile_id,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'address': profile.address
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting admin profile: {e}")
            return None
    
    # def update_admin_profile(self, user_id, first_name, last_name, phone, address):
    #     """Update the admin's profile information"""
    #     try:
    #         # Get user
    #         user = User.find_by_id(user_id)
            
    #         if not user:
    #             return False
            
    #         # Update user phone number
    #         user.phone = phone
            
    #         # Check if user has a profile
    #         profile = UserProfile.find_by_user_id(user_id)
            
    #         if profile:
    #             # Update existing profile
    #             profile.first_name = first_name
    #             profile.last_name = last_name
    #             profile.address = address
    #         else:
    #             # Create new profile
    #             new_profile = UserProfile(
    #                 user_id=user_id,
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 address=address
    #             )
    #             db.session.add(new_profile)
            
    #         db.session.commit()
    #         return True
            
    #     except Exception as e:
    #         print(f"Error updating admin profile: {e}")
    #         db.session.rollback()
    #         return False