from datetime import datetime
from db_config import db
from sqlalchemy import desc, or_

class Booking(db.Model):
    __tablename__ = 'BOOKING'
    
    bookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    homeownerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    serviceID = db.Column(db.Integer, db.ForeignKey('CLEANINGSERVICE.serviceID'))
    cleanerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    bookingDate = db.Column(db.Date)
    bookingHour = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
  
    totalPrice = db.Column(db.Numeric(10, 2))
    bookingStatus = db.Column(db.String(50))
    
    # Relationship with User (homeowner and cleaner)
    homeowner = db.relationship(
        'User', 
        foreign_keys=[homeownerID],
        backref=db.backref('homeowner_bookings', lazy=True)
    )
    
    cleaner = db.relationship(
        'User',
        foreign_keys=[cleanerID],
        backref=db.backref('cleaner_bookings', lazy=True)
    )
    
    def __init__(self, homeownerID, serviceID, cleanerID, bookingDate, bookingHour, totalPrice, bookingStatus):
        self.homeownerID = homeownerID
        self.serviceID = serviceID
        self.cleanerID = cleanerID
        self.bookingDate = bookingDate
        self.bookingHour = bookingHour
        self.totalPrice = totalPrice
        self.bookingStatus = bookingStatus
        
    def to_dict(self):
        return {
            'bookingID': self.bookingID,
            'homeownerID': self.homeownerID,
            'serviceID': self.serviceID,
            'cleanerID': self.cleanerID,
            'bookingDate': self.bookingDate.strftime('%Y-%m-%d') if self.bookingDate else None,
            'bookingHour': self.bookingHour,
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
    
    @classmethod
    def get_bookings_by_cleaner_with_details(cls, cleaner_id):
        """
        Get all bookings for a specific cleaner with homeowner and service details
        
        Args:
            cleaner_id (int): ID of the cleaner
            
        Returns:
            list: List of bookings with associated details
        """
        from entity.UserAccount import User
        from entity.CleaningService import CleaningService
        
        return db.session.query(
            cls,
            User,
            CleaningService
        ).join(
            User, cls.homeownerID == User.userID
        ).join(
            CleaningService, cls.serviceID == CleaningService.serviceID
        ).filter(
            cls.cleanerID == cleaner_id
        ).order_by(
            cls.bookingDate.desc()
        ).all()
    
    @classmethod
    def filter_bookings_by_status_with_details(cls, cleaner_id, status):
        """
        Filter bookings by status for a cleaner with all associated details
        
        Args:
            cleaner_id (int): ID of the cleaner
            status (str): Status to filter by
            
        Returns:
            list: List of filtered bookings with details
        """
        from entity.UserAccount import User
        from entity.CleaningService import CleaningService
        
        return db.session.query(
            cls,
            User,
            CleaningService
        ).join(
            User, cls.homeownerID == User.userID
        ).join(
            CleaningService, cls.serviceID == CleaningService.serviceID
        ).filter(
            cls.cleanerID == cleaner_id,
            cls.bookingStatus == status
        ).order_by(
            cls.bookingDate.desc()
        ).all()
    
    @classmethod
    def get_homeowner_bookings_with_details(cls, homeowner_id, status=None):
        """
        Get all bookings for a homeowner with optional status filter and related details
        
        Args:
            homeowner_id (int): ID of the homeowner
            status (str, optional): Filter by booking status
            
        Returns:
            list: List of tuples containing (booking, cleaner, service)
        """
        try:
            from entity.UserAccount import User
            from entity.CleaningService import CleaningService
            
            # Start query
            query = (
                db.session.query(
                    cls,
                    User,
                    CleaningService
                )
                .join(User, cls.cleanerID == User.userID)
                .join(CleaningService, cls.serviceID == CleaningService.serviceID)
                .filter(cls.homeownerID == homeowner_id)
            )
            
            # Add status filter if provided
            if status:
                query = query.filter(cls.bookingStatus == status)
            
            # Execute query
            results = query.order_by(cls.bookingDate.desc()).all()
            
            return results
        except Exception as e:
            print(f"Error getting homeowner bookings: {str(e)}")
            return []
    
    @classmethod
    def search_homeowner_bookings(cls, homeowner_id, keyword):
        """
        Search bookings for a homeowner by keyword
        
        Args:
            homeowner_id (int): ID of the homeowner
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (booking, cleaner, service)
        """
        try:
            from entity.UserAccount import User
            from entity.CleaningService import CleaningService
            
            # Search in service title, cleaner name, and booking status
            search_term = f"%{keyword}%"
            
            query = (
                db.session.query(
                    cls,
                    User,
                    CleaningService
                )
                .join(User, cls.cleanerID == User.userID)
                .join(CleaningService, cls.serviceID == CleaningService.serviceID)
                .filter(cls.homeownerID == homeowner_id)
                .filter(
                    or_(
                        CleaningService.title.ilike(search_term),
                        User.first_name.ilike(search_term),
                        User.last_name.ilike(search_term),
                        cls.bookingStatus.ilike(search_term)
                    )
                )
            )
            
            # Execute query and order by booking date (newest first)
            results = query.order_by(cls.bookingDate.desc()).all()
            
            return results
        except Exception as e:
            print(f"Error searching homeowner bookings: {str(e)}")
            return []
    
    @classmethod
    def create_new_booking(cls, homeowner_id, service_id, cleaner_id, booking_date, hours, total_price):
        """
        Create a new booking
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            cleaner_id (int): ID of the cleaner
            booking_date (datetime): Date of the booking
            hours (int): Number of hours for the booking
            total_price (float): Total price of the booking
            
        Returns:
            Booking: The created booking object
        """
        booking = cls(
            homeownerID=homeowner_id,
            serviceID=service_id,
            cleanerID=cleaner_id,
            bookingDate=booking_date,
            bookingHour=hours,
            totalPrice=total_price,
            bookingStatus='Pending'
        )
        
        booking.save_to_db()
        return booking
        
    def save_to_db(self):
        """Save booking to database"""
        db.session.add(self)
        db.session.commit()
    
        
    def update_status(self, new_status):
        """Update booking status"""
        self.bookingStatus = new_status
        db.session.commit()
        return True