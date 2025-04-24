from datetime import datetime
from db_config import db

class User(db.Model):
    __tablename__ = 'users'
    
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)
    
    # Relationship with UserProfile
    profile = db.relationship('UserProfile', backref='user', lazy=True, uselist=False)
    
    def __init__(self, email, password, role, phone=None):
        self.email = email
        self.password = password  # In a real application, you'd hash this password
        self.role = role
        self.phone = phone
        
    def to_dict(self):
        return {
            'userID': self.userID,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at,
            'isActive': self.isActive
        }

class UserProfile(db.Model):
    __tablename__ = 'userprofiles'
    
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    isActive = db.Column(db.Boolean, default=True)
    
    def __init__(self, user_id, first_name, last_name, address=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        
    def to_dict(self):
        return {
            'profile_id': self.profile_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address
        }