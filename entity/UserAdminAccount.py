from db_config import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

    
class User(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    userID = db.Column(db.Integer, primary_key=True)  # ← THIS is your actual PK
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return self.password == password


    
    
