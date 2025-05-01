from datetime import datetime
from db_config import db

class Category(db.Model):
    __tablename__ = 'CATEGORY'
    __table_args__ = {'extend_existing': True}
    
    categoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    categoryStatus = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # # Relationship with CleaningService
    # services = db.relationship('CleaningService', backref='category', lazy=True)
    
    def __init__(self, name, description, categoryStatus=True):
        self.name = name
        self.description = description
        self.categoryStatus = categoryStatus
    
    def to_dict(self):
        """Convert category object to dictionary with human-readable status"""
        return {
            'categoryID': self.categoryID,
            'name': self.name,
            'description': self.description,
            'categoryStatus': self.categoryStatus,
            'create_at': self.create_at
        }
    
    # Database operations
    @classmethod
    def find_by_id(cls, category_id):
        """Find a category by ID"""
        return cls.query.get(category_id)

    @classmethod
    def find_by_name(cls, name):
        """Check if a category with the same name already exists"""
        return cls.query.filter_by(name=name).first()

    
    @classmethod
    def get_all(cls):
        """Get all categories"""
        return cls.query.all()
    
    @classmethod
    def search_by_keyword(cls, keyword):
        """Search categories by name or description"""
        from sqlalchemy import or_
        return cls.query.filter(
            or_(
                cls.name.ilike(f'%{keyword}%'),
                cls.description.ilike(f'%{keyword}%')
            )
        ).all()
    
    def save_to_db(self):
        """Save category to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete category from database"""
        db.session.delete(self)
        db.session.commit()
        
    def update_in_db(self, name, description, categoryStatus):
        """Update category attributes"""
        self.name = name
        self.description = description
        self.categoryStatus = categoryStatus
        db.session.commit()
        return True

    def suspend(self):
        """Suspend a category by setting categoryStatus to False"""
        self.categoryStatus = False
        db.session.commit()
        return True

    def reactivate(self):
        """Reactivate a category by setting categoryStatus to True"""
        self.categoryStatus = True
        db.session.commit()
        return True