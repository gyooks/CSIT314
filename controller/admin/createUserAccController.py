# from werkzeug.security import generate_password_hash
from entity.UserAccount import User
from entity.UserProfile import UserProfile
from db_config import db

class createUserAccController:
    @staticmethod
    def create_user(email, password, role, phone=None, first_name=None, last_name=None, address=None):
        """
        Create a new user with profile information
        """
        try:
            # Check if user with this email already exists
            existing_user = User.find_by_email(email)
            if existing_user:
                return False, "Email already exists"
            
            # Create new user
            new_user = User(
                email=email,
                password=password,
                role=role,
                phone=phone
            )
            
            # Add to session and flush to get the user ID
            db.session.add(new_user)
            db.session.flush()
            
            # Create user profile if profile info provided
            if first_name or last_name:
                user_profile = UserProfile(
                    user_id=new_user.userID,
                    first_name=first_name,
                    last_name=last_name,
                    address=address
                )
                db.session.add(user_profile)
            
            # Commit changes
            db.session.commit()
            return True, "User created successfully"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error creating user: {str(e)}"