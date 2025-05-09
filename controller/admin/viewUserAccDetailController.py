from entity.UserAccount import User

class viewUserAccDetailController:
    
    @staticmethod
    def get_user_with_details(user_id):
        """
        Get a single user with full profile information
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            dict: User information with profile details or None if not found
            str: Error message if any, None if successful
        """
        try:
            # Use the entity layer to fetch user by ID
            user = User.find_by_id(user_id)
            
            if not user:
                return None, "User not found"
                
            # Convert user to dictionary format with complete details
            user_dict = user.to_dict()
            
            # Add any additional processing or data enrichment here if needed
            
            return user_dict, None
            
        except Exception as e:
            print(f"Error retrieving user details: {e}")
            return None, f"Error retrieving user details: {str(e)}"
    
  