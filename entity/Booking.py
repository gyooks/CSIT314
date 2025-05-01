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
    totalPrice = db.Column(db.Numeric(10, 2))
    bookingStatus = db.Column(db.String(50))
    
    def __init__(self, homeownerID, serviceID, cleanerID, bookingDate, totalPrice, bookingStatus):
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
            'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S') if self.create_at else None,
            'totalPrice': float(self.totalPrice) if self.totalPrice else None,
            'bookingStatus': self.bookingStatus
        }
    
    @classmethod
    def find_by_id(cls, booking_id):
        """Find a booking by ID"""
        return cls.query.get(booking_id)
    
    @classmethod
    def get_bookings_by_date_range(cls, start_date, end_date):
        """Get all bookings within a date range"""
        return cls.query.filter(
            cls.bookingDate >= start_date,
            cls.bookingDate <= end_date
        ).all()
    
    @classmethod
    def get_bookings_by_homeowner(cls, homeowner_id):
        """Get all bookings for a specific homeowner"""
        return cls.query.filter_by(homeownerID=homeowner_id).all()
    
    @classmethod
    def get_bookings_by_cleaner(cls, cleaner_id):
        """Get all bookings for a specific cleaner"""
        return cls.query.filter_by(cleanerID=cleaner_id).all()
    
    @classmethod
    def get_bookings_by_status(cls, status):
        """Get all bookings with a specific status"""
        return cls.query.filter_by(bookingStatus=status).all()
        
    def save_to_db(self):
        """Save booking to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Delete booking from database"""
        db.session.delete(self)
        db.session.commit()
        
    def update_status(self, new_status):
        """Update booking status"""
        self.bookingStatus = new_status
        db.session.commit()
        return True