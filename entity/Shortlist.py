from datetime import datetime
from db_config import db
from sqlalchemy import or_

class Shortlist(db.Model):
    __tablename__ = 'SHORTLIST'
    
    shortlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    homeownerID = db.Column(db.Integer, db.ForeignKey('USERS.userID'))
    serviceID = db.Column(db.Integer, db.ForeignKey('CLEANINGSERVICE.serviceID'))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    homeowner = db.relationship(
        'User', 
        foreign_keys=[homeownerID],
        backref=db.backref('shortlisted_services', lazy=True)
    )
    
    service = db.relationship(
        'CleaningService',
        backref=db.backref('shortlisted_by', lazy=True),
        foreign_keys=[serviceID]
    )
    
    def __init__(self, homeownerID, serviceID):
        self.homeownerID = homeownerID
        self.serviceID = serviceID
        
    def to_dict(self):
        return {
            'shortlistID': self.shortlistID,
            'homeownerID': self.homeownerID,
            'serviceID': self.serviceID,
            'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S') if self.create_at else None
        }
    
    @classmethod
    def find_existing_shortlist(cls, homeowner_id, service_id):
        """
        Find an existing shortlist entry
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            Shortlist or None: The shortlist entry if found, None otherwise
        """
        return cls.query.filter_by(
            homeownerID=homeowner_id, 
            serviceID=service_id
        ).first()
    
    @classmethod
    def is_service_shortlisted(cls, homeowner_id, service_id):
        """
        Check if a service is shortlisted by a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            bool: True if service is shortlisted, False otherwise
        """
        try:
            shortlist = cls.find_existing_shortlist(homeowner_id, service_id)
            return shortlist is not None
        except Exception as e:
            print(f"Error checking if service is shortlisted: {str(e)}")
            return False
    
    @classmethod
    def get_shortlisted_service_ids(cls, homeowner_id):
        """
        Get list of service IDs shortlisted by a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of shortlisted service IDs
        """
        try:
            shortlisted = cls.query.filter_by(homeownerID=homeowner_id).all()
            return [item.serviceID for item in shortlisted]
        except Exception as e:
            print(f"Error getting shortlisted services: {str(e)}")
            return []
    
    @classmethod
    def add_service(cls, homeowner_id, service_id):
        """
        Add a service to the homeowner's shortlist
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create new shortlist entry
            shortlist = cls(homeownerID=homeowner_id, serviceID=service_id)
            db.session.add(shortlist)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding to shortlist: {str(e)}")
            return False
    
    @classmethod
    def remove_service(cls, shortlist_entry):
        """
        Remove a service from the homeowner's shortlist
        
        Args:
            shortlist_entry (Shortlist): The shortlist entry to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            db.session.delete(shortlist_entry)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error removing from shortlist: {str(e)}")
            return False
    
    @classmethod
    def get_homeowner_shortlist(cls, homeowner_id):
        """
        Get all shortlisted services for a homeowner with service and cleaner info
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of tuples containing (shortlist, service, cleaner, category)
        """
        try:
            from entity.CleaningService import CleaningService
            from entity.UserAccount import User
            from entity.Category import Category
            
            # Query shortlisted services with service, cleaner and category data
            results = (
                db.session.query(
                    cls,
                    CleaningService,
                    User,
                    Category
                )
                .join(CleaningService, cls.serviceID == CleaningService.serviceID)
                .join(User, CleaningService.cleanerID == User.userID)
                .join(Category, CleaningService.categoryID == Category.categoryID)
                .filter(cls.homeownerID == homeowner_id)
                .filter(CleaningService.serviceStatus == True)
                .filter(User.isActive == True)
                .all()
            )
            
            return results
        except Exception as e:
            print(f"Error getting homeowner shortlist: {str(e)}")
            return []

    @classmethod
    def search_homeowner_shortlist(cls, homeowner_id, keyword):
        """
        Search through homeowner's shortlisted services
        
        Args:
            homeowner_id (int): ID of the homeowner
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (shortlist, service, cleaner, category)
        """
        try:
            from entity.CleaningService import CleaningService
            from entity.UserAccount import User
            from entity.Category import Category
            
            # Prepare search keyword
            search_term = f"%{keyword}%"
            
            # Query shortlisted services matching search term
            results = (
                db.session.query(
                    cls,
                    CleaningService,
                    User,
                    Category
                )
                .join(CleaningService, cls.serviceID == CleaningService.serviceID)
                .join(User, CleaningService.cleanerID == User.userID)
                .join(Category, CleaningService.categoryID == Category.categoryID)
                .filter(cls.homeownerID == homeowner_id)
                .filter(CleaningService.serviceStatus == True)
                .filter(User.isActive == True)
                .filter(
                    or_(
                        CleaningService.title.ilike(search_term),
                        CleaningService.description.ilike(search_term),
                        Category.name.ilike(search_term),
                        User.first_name.ilike(search_term),
                        User.last_name.ilike(search_term)
                    )
                )
                .all()
            )
            
            return results
        except Exception as e:
            print(f"Error searching homeowner shortlist: {str(e)}")
            return []

    @classmethod
    def get_recent_by_service(cls, service_id, limit=5):
        """
        Get recent shortlists for a specific service
        show in cleaning service detail for cleaner
        
        Args:
            service_id (int): ID of the service
            limit (int): Maximum number of shortlists to return
        
        Returns:
            list: List of recent Shortlist objects
        """
        return (cls.query
                .filter_by(serviceID=service_id)
                .order_by(cls.create_at.desc())
                .limit(limit)
                .all())