from db_config import db

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
    
    # Database operations - moved from controllers to entity
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find a profile by user ID"""
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_profile_id(cls, profile_id):
        """Find a profile by profile ID"""
        return cls.query.get(profile_id)
    
    def save_to_db(self):
        """Save profile to database"""
        db.session.add(self)
        db.session.commit()
        
    def update_in_db(self, first_name, last_name, address):
        """Update profile attributes"""
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        db.session.commit()
        return True