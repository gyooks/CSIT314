from datetime import datetime
from db_config import db

class CleaningService(db.Model):
    __tablename__ = 'CLEANINGSERVICE'
    __table_args__ = {'extend_existing': True}
    
    serviceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cleanerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    categoryID = db.Column(db.Integer, db.ForeignKey('CATEGORY.categoryID'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2))
    serviceStatus = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, cleanerID, categoryID, title, description, price, serviceStatus=True):
        self.cleanerID = cleanerID
        self.categoryID = categoryID
        self.title = title
        self.description = description
        self.price = price
        self.serviceStatus = serviceStatus
    
    def to_dict(self):
        return {
            'serviceID': self.serviceID,
            'cleanerID': self.cleanerID,
            'categoryID': self.categoryID,
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'serviceStatus': 'Active' if self.serviceStatus else 'Inactive',
            'create_at': self.create_at
        }