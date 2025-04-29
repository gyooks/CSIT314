from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from db_config import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)
    
    # Relationship with UserProfile
    profile = db.relationship(
        'UserProfile',
        backref='user',
        lazy=True,
        uselist=False,
        foreign_keys='UserProfile.user_id'  
    )
    
    # Constructor: initializes the object with given values
    def __init__(self, email, password, role, phone=None):
        self.email = email
        self.password = password  # In a real application, you'd hash this password
        self.role = role
        self.phone = phone
    
    # Converts object into a dictionary format
    def to_dict(self):
        return {
            'userID': self.userID,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at,
            'isActive': self.isActive
        }

    def verify_password(self, password):
        #return check_password_hash(self.password, password) 
        return self.password == password
    
    # Database operations - moved from controllers to entity
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by ID"""
        return cls.query.get(user_id)
    
    @classmethod
    def get_all(cls):
        """Get all users"""
        return cls.query.all()
    
    @classmethod
    def search_with_profiles(cls, keyword):
        """Search users by keyword and join with profiles"""
        from sqlalchemy import or_
        from entity.UserProfile import UserProfile
        
        return db.session.query(cls, UserProfile).outerjoin(
            UserProfile, cls.userID == UserProfile.user_id
        ).filter(
            or_(
                cls.email.ilike(f'%{keyword}%'),
                cls.phone.ilike(f'%{keyword}%'),
            )
        ).all()
    
    def save_to_db(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete user from database"""
        db.session.delete(self)
        db.session.commit()
        
    def update_in_db(self, email, phone, role, is_active):
        """Update user attributes"""
        self.email = email
        self.phone = phone
        self.role = role
        self.isActive = is_active
        db.session.commit()
        return True
        
    def suspend(self):
        """Suspend a user by setting isActive to False"""
        self.isActive = False
        db.session.commit()
        return True
    
    def reactivate(self):
        """Reactivate a user by setting isActive to True"""
        self.isActive = True
        db.session.commit()
        return True