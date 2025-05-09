from entity.UserAccount import User
from db_config import db

class SearchUserAccController:
    
    @staticmethod
    def search_users(keyword):
        """
        Search users by keyword
        The search looks in email, first_name, last_name, address, phone
        and role_name (joined from UserProfile)
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of matching users as dictionaries
        """
        try:
            # Use the search_users method from the User entity
            users = User.search_users(keyword)
            
            if not users:
                return []
                
            # Convert users to dictionary format
            user_list = []
            for user in users:
                user_dict = user.to_dict()
                user_list.append(user_dict)
                
            return user_list
            
        except Exception as e:
            print(f"Error searching users: {e}")
            return []
            
    