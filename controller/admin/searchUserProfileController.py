from entity.UserProfile import UserProfile

class SearchProfileController:
    @staticmethod
    def search_profiles(keyword):
        
        # Use the entity's search method
        return UserProfile.search_profiles(keyword)