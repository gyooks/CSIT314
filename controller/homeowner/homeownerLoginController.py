from entity.UserAccount import User
from flask import session

class LoginController:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return False, "Incorrect User or Password"
            
        # Check if user account is inactive
        if not user.isActive:
            return False, "Account is inactive. Please contact an administrator."
        
        # Check if user is homeowner
        if not user.profile or user.profile.role_name != "Homeowner":
            return False, "Access denied. Only homeowner can login here."
            
        if user.verify_password(password):
            session['user_id'] = user.userID #save login state
            return True, "Login successful"
            
        return False, "Incorrect User or Password"