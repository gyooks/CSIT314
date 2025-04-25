from entity.UserAdminAccount import User
from flask import session

class LoginController:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "User not found"
        if user.verify_password(password):
            session['user_id'] = user.userID #save login state
            return True, "Login successful"
        return False, "Incorrect password"