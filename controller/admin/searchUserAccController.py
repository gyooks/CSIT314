from entity.UserAccount import User
from entity.UserProfile import UserProfile

class SearchUserAccController:
    def search_userAcc(self, keyword):
        # Use the search method from User entity
        return User.search_with_profiles(keyword)