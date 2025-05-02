from werkzeug.security import generate_password_hash
from entity.UserAccount import User

class createUserAccController:
    @staticmethod
    def create_user(email, password, role):
        """
        Create a new user account
        
        Returns:
            tuple: (success_bool, message_str, user_id)
        """
        try:
            # Check if user with this email already exists
            existing_user = User.find_by_email(email)
            if existing_user:
                return False, "Email already exists", None
                
            # Create new user
            new_user = User(
                email=email,
                password=generate_password_hash(password),
                role=role
            )
            
            # Save to db through entity
            new_user.save_to_db()
            
            # Return the new user ID for profile creation
            return True, "User account created successfully", new_user.userID
                
        except Exception as e:
            return False, f"Error creating user account: {str(e)}", None