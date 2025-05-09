from datetime import datetime
from db_config import db

class User(db.Model):
    __tablename__ = 'USERS'
    __table_args__ = {'extend_existing': True}
    
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('USERPROFILE.role_id'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)
    
    # Constructor: initializes the object with given values
    def __init__(self, email, password, role_id, first_name=None, last_name=None, 
                 address=None, phone=None):
        self.email = email
        self.password = password  # Now stored as plain text
        self.role_id = role_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
    
    # Converts object into a dictionary format
    def to_dict(self):
        """Converts object into a dictionary format with role name included"""
        user_dict = {
            'userID': self.userID,
            'email': self.email,
            'role_id': self.role_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at,
            'isActive': self.isActive
        }
        
        # Always include role name
        if hasattr(self, 'profile') and self.profile:
            user_dict['role_name'] = self.profile.role_name
            # Create a profile dictionary to match the template's expectations
            user_dict['profile'] = {
                'role_name': self.profile.role_name
            }
        
        return user_dict

    def verify_password(self, password):
        # Direct string comparison instead of hash verification
        return self.password == password
    
    # Database operations
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by ID with eager loading of profile"""
        return cls.query.options(db.joinedload(cls.profile)).get(user_id)
    
    @classmethod
    def get_all(cls):
        """Get all users with eager loading of profiles"""
        return cls.query.options(db.joinedload(cls.profile)).all()
    
    
    @classmethod
    def search_users(cls, keyword):
        """Search users by keyword and join with profiles"""
        from sqlalchemy import or_
        from entity.UserProfile import UserProfile
        
        query = db.session.query(cls).join(
            UserProfile, cls.role_id == UserProfile.role_id
        ).filter(
            or_(
                cls.email.ilike(f'%{keyword}%'),
                UserProfile.role_name.ilike(f'%{keyword}%'),
                cls.first_name.ilike(f'%{keyword}%'),
                cls.last_name.ilike(f'%{keyword}%'),
                cls.address.ilike(f'%{keyword}%'),
                cls.phone.ilike(f'%{keyword}%')
            )
        )
        
        return query.all()
    
    @classmethod
    def get_users_by_role(cls, role_id):
        """Get all users with a specific role"""
        return cls.query.filter_by(role_id=role_id).all()
    
    @staticmethod
    def get_role_id_by_name(role_name):
        """Utility method to get role_id from role_name"""
        from entity.UserProfile import UserProfile
        profile = UserProfile.find_by_name(role_name)
        return profile.role_id if profile else None
    
    def save_to_db(self):
        """Save user to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_in_db(self, email=None, role_id=None, password=None, 
                    first_name=None, last_name=None, address=None, 
                    phone=None):
        """Update user attributes"""
        if email is not None:
            self.email = email
        if role_id is not None:
            self.role_id = role_id
        if password is not None and password.strip() != '':
            # Only update password if not empty
            self.password = password  # Store password as plain text
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if address is not None:
            self.address = address
        if phone is not None:
            self.phone = phone

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
        
    @classmethod
    def search_by_name(cls, name_query):
        """Search users by first or last name"""
        from sqlalchemy import or_
        return cls.query.filter(
            or_(
                cls.first_name.ilike(f'%{name_query}%'),
                cls.last_name.ilike(f'%{name_query}%')
            )
        ).all()
        
    @classmethod
    def search_by_role(cls, role_name):
        """Search users by role name"""
        from entity.UserProfile import UserProfile
        
        return cls.query.join(
            UserProfile, cls.role_id == UserProfile.role_id
        ).filter(
            UserProfile.role_name.ilike(f'%{role_name}%')
        ).all()