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
            

            
