from db_config import db
from sqlalchemy import or_

class UserProfile(db.Model):
    __tablename__ = 'userprofiles'
    
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    isActive = db.Column(db.Boolean, default=True)
    
    def __init__(self, user_id, first_name, last_name, address=None, phone=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        
    def to_dict(self):
        return {
            'profile_id': self.profile_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'phone': self.phone,
            'isActive': self.isActive
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
    
    @classmethod
    def get_all(cls):
        """Get all users"""
        return cls.query.all()
    
    @classmethod
    def search_profiles(cls, keyword):
        """Search profiles by keyword"""
        return cls.query.filter(
            or_(
                cls.first_name.ilike(f'%{keyword}%'),
                cls.last_name.ilike(f'%{keyword}%'),
                cls.address.ilike(f'%{keyword}%'),
                cls.phone.ilike(f'%{keyword}%')
            )
        ).all()

    def save_to_db(self):
        """Save profile to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_in_db(self, first_name, last_name, address, phone):
        """Update profile attributes"""
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        db.session.commit()
        return True
        
    def delete_from_db(self):
        """Delete profile from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
            
    def suspend(self):
        """Suspend a profile by setting isActive to False"""
        self.isActive = False
        db.session.commit()
        return True
    
    def reactivate(self):
        """Reactivate a profile by setting isActive to True"""
        self.isActive = True
        db.session.commit()
        return True