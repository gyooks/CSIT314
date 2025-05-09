from werkzeug.security import generate_password_hash
from entity.UserAccount import User
from db_config import db

class createUserAccController:
    @staticmethod
    def create_user(email, password, role_id, first_name, last_name, address=None, phone=None):
        """
        Create a new user with all profile information
        
        Args:
            email (str): User email
            password (str): User password
            role_id (int): ID of the profile/role from the USERPROFILE table
            first_name (str): User's first name
            last_name (str): User's last name
            address (str, optional): User's address
            phone (str, optional): User's phone number
            
        Returns:
            tuple: (success_bool, message_str, user_id)
        """
        try:
            # Check if user with this email already exists
            existing_user = User.find_by_email(email)
            if existing_user:
                return False, "Email already exists", None
                
            # Create new user with all information
            new_user = User(
                email=email,
                password=generate_password_hash(password),
                role_id=role_id,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone
            )
            
            # Validate required fields
            if not first_name or not last_name:
                return False, "First name and last name are required", None
            
            # Save user to database
            success = new_user.save_to_db()
            
            if success:
                return True, "User created successfully", new_user.userID
            else:
                return False, "Error creating user", None
                
        except Exception as e:
            return False, f"Error creating user: {str(e)}", None