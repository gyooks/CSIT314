from datetime import datetime
from db_config import db

class Shortlist(db.Model):
    __tablename__ = 'SHORTLIST'
    
    shortlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    homeownerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    serviceID = db.Column(db.Integer, db.ForeignKey('CLEANINGSERVICE.serviceID'))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    homeowner = db.relationship('User', backref='shortlisted_services')
    
    def __init__(self, homeownerID, serviceID):
        self.homeownerID = homeownerID
        self.serviceID = serviceID
        
    def to_dict(self):
        return {
            'shortlistID': self.shortlistID,
            'homeownerID': self.homeownerID,
            'serviceID': self.serviceID,
            'create_at': self.create_at
        }