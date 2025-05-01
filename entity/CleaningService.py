from datetime import datetime
from db_config import db

class CleaningService(db.Model):
    __tablename__ = 'CLEANINGSERVICE'
    
    serviceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cleanerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    categoryID = db.Column(db.Integer, db.ForeignKey('CATEGORY.categoryID'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    serviceStatus = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, cleanerID, categoryID, title, description, price):
        self.cleanerID = cleanerID
        self.categoryID = categoryID
        self.title = title
        self.description = description
        self.price = price
        
    def to_dict(self):
        return {
            'serviceID': self.serviceID,
            'cleanerID': self.cleanerID,
            'categoryID': self.categoryID,
            'title': self.title,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'serviceStatus': self.serviceStatus,
            'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S') if self.create_at else None
        }
    
    @classmethod
    def find_by_id(cls, service_id):
        """Find a cleaning service by ID"""
        return cls.query.get(service_id)
    
    @classmethod
    def find_by_cleaner(cls, cleaner_id):
        """Find all cleaning services by a specific cleaner"""
        return cls.query.filter_by(cleanerID=cleaner_id).all()
    
    @classmethod
    def find_by_category(cls, category_id):
        """Find all cleaning services by category"""
        return cls.query.filter_by(categoryID=category_id).all()
    
    @classmethod
    def find_active_services(cls):
        """Find all active cleaning services"""
        return cls.query.filter_by(serviceStatus=True).all()
        
    def save_to_db(self):
        """Save cleaning service to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete cleaning service from database"""
        db.session.delete(self)
        db.session.commit()
        
    def update_service(self, title, description, price, category_id):
        """Update cleaning service details"""
        self.title = title
        self.description = description
        self.price = price
        self.categoryID = category_id
        db.session.commit()
        return True
        
    def toggle_status(self):
        """Toggle service active status"""
        self.serviceStatus = not self.serviceStatus
        db.session.commit()
        return True