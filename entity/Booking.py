from datetime import datetime
from db_config import db

class Booking(db.Model):
    __tablename__ = 'BOOKING'
    
    bookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    homeownerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    serviceID = db.Column(db.Integer, db.ForeignKey('CLEANINGSERVICE.serviceID'))
    cleanerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    bookingDate = db.Column(db.Date)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    totalPrice = db.Column(db.Decimal(10, 2))
    bookingStatus = db.Column(db.String(50))
    
    # Relationships
    homeowner = db.relationship('User', foreign_keys=[homeownerID], backref='bookings_made')
    cleaner = db.relationship('User', foreign_keys=[cleanerID], backref='bookings_received')
    
    def __init__(self, homeownerID, serviceID, cleanerID, bookingDate, totalPrice, bookingStatus='Pending'):
        self.homeownerID = homeownerID
        self.serviceID = serviceID
        self.cleanerID = cleanerID
        self.bookingDate = bookingDate
        self.totalPrice = totalPrice
        self.bookingStatus = bookingStatus
        
    def to_dict(self):
        return {
            'bookingID': self.bookingID,
            'homeownerID': self.homeownerID,
            'serviceID': self.serviceID,
            'cleanerID': self.cleanerID,
            'bookingDate': self.bookingDate.strftime('%Y-%m-%d') if self.bookingDate else None,
            'create_at': self.create_at,
            'totalPrice': float(self.totalPrice),
            'bookingStatus': self.bookingStatus
        }