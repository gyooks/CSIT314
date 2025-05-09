from entity.UserAccount import User
from flask import session  

class LoginController:
    def login(self, email, password):
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return False, "Incorrect User or Password"
        
        # Check if user account is inactive
        if not user.isActive:
            return False, "Account is inactive. Please contact an administrator."
        
        if not user.profile or user.profile.role_name != "User admin":
            return False, "Access denied. Only administrators can login here."
        
        if user.verify_password(password):
            # Save login state
            session['user_id'] = user.userID
            # Store profile information in the session
            session['role_name'] = user.profile.role_name
            return True, "Login successful"
        
        return False, "Incorrect User or Password"