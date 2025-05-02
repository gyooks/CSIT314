from entity.UserProfile import UserProfile

class viewUserProfileController:
    @staticmethod
    def get_all_profiles():
        """
        Get all users from database
        """
        try:
            userprofiles = UserProfile.get_all()
            return [profile.to_dict() for profile in userprofiles]
        except Exception as e:
            return []
    
            

    
