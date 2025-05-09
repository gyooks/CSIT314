from entity.UserAccount import User

class viewUserAccController:
    
    @staticmethod
    def get_all_users():
        """
        Get all users with their profile information
        """
        try:
            users = User.get_all()
            
            if not users:
                return []
                
            # Convert users to dictionary format
            user_list = []
            for user in users:
                user_dict = user.to_dict()
                user_list.append(user_dict)
                
            return user_list
            
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
            
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get a specific user by ID
        """
        try:
            user = User.find_by_id(user_id)
            
            if not user:
                return None
                
            return user.to_dict()
            
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
            
