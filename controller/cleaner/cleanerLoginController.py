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
        
        if not user.profile or user.profile.role_name != "Cleaner":
            return False, "Access denied. Only cleaner can login here."
            
        if user.verify_password(password):
            session['user_id'] = user.userID #save login state
            return True, "Login successful"
            
        return False, "Incorrect User or Password"