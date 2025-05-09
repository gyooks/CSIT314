from entity.UserProfile import UserProfile

class ViewUserProfileController:
            
    @staticmethod
    def get_all_profiles():
        """Get all user profiles/roles"""
        return UserProfile.get_all()
    
