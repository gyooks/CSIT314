from entity.UserAdminAccount import User

class LoginController:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "User not found"
        if user.verify_password(password):
            return True, "Login successful"
        return False, "Incorrect password"
