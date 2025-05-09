from db_config import db
from sqlalchemy import or_

class UserProfile(db.Model):
    __tablename__ = 'USERPROFILE'
    __table_args__ = {'extend_existing': True}
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    roleStatus = db.Column(db.Boolean, default=True)
    
    # Relationship with User
    users = db.relationship(
        'User',
        backref='profile',
        lazy=True,
        foreign_keys='User.role_id'
    )
    
    def __init__(self, role_name, description=None):
        self.role_name = role_name
        self.description = description
        
    def to_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'description': self.description,
            'roleStatus': self.roleStatus,
        }
        
    # Database operations
    @classmethod
    def find_by_id(cls, role_id):
        """Find a user profile by ID"""
        return cls.query.get(role_id)
    
    @classmethod
    def find_by_name(cls, role_name):
        """Find a user profile by name"""
        return cls.query.filter_by(role_name=role_name).first()
    
    @classmethod
    def get_all(cls):
        """Get all user profiles"""
        return cls.query.all()
    
    def save_to_db(self):
        """Save user profile to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def get_users_count(cls, role_id):
        """Get the number of users assigned to this profile/role"""
        profile = cls.find_by_id(role_id)
        if profile:
            return len(profile.users)
        return 0
    
    def update_in_db(self, role_name, description):
        """Update user profile attributes"""
        self.role_name = role_name
        self.description = description
        db.session.commit()
        return True

    @classmethod
    def get_all_active(cls):
        """Get all active user profiles"""
        return cls.query.filter_by(roleStatus=True).all()

    def suspend(self):
        """Suspend a user profile by setting roleStatus to False"""
        self.roleStatus = False
        db.session.commit()
        return True

    def reactivate(self):
        """Reactivate a user profile by setting roleStatus to True"""
        self.roleStatus = True
        db.session.commit()
        return True
        
    @classmethod
    def search_profiles(cls, keyword):
        """Search user profiles by name or description"""
        # Convert keyword to lowercase for case-insensitive search
        search_term = f"%{keyword.lower()}%"
        
        # Search by name or description
        return cls.query.filter(
            or_(
                cls.role_name.ilike(search_term),
                cls.description.ilike(search_term)
            )
        ).all()