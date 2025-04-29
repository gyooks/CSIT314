from flask import session

class LogoutController:
    def logout(self):
        session.pop('user_id', None)
