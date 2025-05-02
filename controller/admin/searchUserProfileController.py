from entity.UserProfile import UserProfile

class SearchProfileController:
    @staticmethod
    def search_profiles(keyword):
        """
        Search for user profiles by keyword
        
        Args:
            keyword (str): The search keyword
            
        Returns:
            list: List of matching user profiles
        """
        try:
            profiles = UserProfile.search_profiles(keyword)
            return [profile.to_dict() for profile in profiles]
        except Exception as e:
            return []