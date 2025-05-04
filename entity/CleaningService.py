from datetime import datetime
from db_config import db
from sqlalchemy import or_, and_
from entity.UserAccount import User
from entity.Category import Category
from entity.UserProfile import UserProfile

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
    
    # Define the relationship with Category
    category = db.relationship(
        'Category',
        backref=db.backref('services', lazy=True),
        lazy='joined',  
        foreign_keys=[categoryID]
    )
    
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
    
    @classmethod
    def get_all_services_with_details(cls):
        """
        Get all active cleaning services with cleaner info for homeowner view
        
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        try:
            # Query active services with cleaner, profile, and category data
            results = (
                db.session.query(
                    cls,
                    User,
                    UserProfile,
                    Category
                )
                .join(User, cls.cleanerID == User.userID)
                .join(UserProfile, User.userID == UserProfile.user_id)
                .join(Category, cls.categoryID == Category.categoryID)
                .filter(cls.serviceStatus == True)
                .filter(User.isActive == True)
                .filter(Category.categoryStatus == True)
                .all()
            )
            
            return results
        except Exception as e:
            print(f"Error getting services: {str(e)}")
            return []
    
    @classmethod
    def get_services_by_category_with_details(cls, category_id):
        """
        Get active cleaning services filtered by category with cleaner info
        
        Args:
            category_id (int): ID of the category to filter by
            
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        try:
            # Query active services filtered by category
            results = (
                db.session.query(
                    cls,
                    User,
                    UserProfile,
                    Category
                )
                .join(User, cls.cleanerID == User.userID)
                .join(UserProfile, User.userID == UserProfile.user_id)
                .join(Category, cls.categoryID == Category.categoryID)
                .filter(cls.serviceStatus == True)
                .filter(User.isActive == True)
                .filter(Category.categoryStatus == True)
                .filter(cls.categoryID == category_id)
                .all()
            )
            
            return results
        except Exception as e:
            print(f"Error getting services by category: {str(e)}")
            return []
    
    @classmethod
    def search_services_with_details(cls, keyword):
        """
        Search active cleaning services by keyword with cleaner info
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        try:
            # If no keyword provided, return all services
            if not keyword or not keyword.strip():
                return cls.get_all_services_with_details()
            
            # Query active services filtered by keyword
            results = (
                db.session.query(
                    cls,
                    User,
                    UserProfile,
                    Category
                )
                .join(User, cls.cleanerID == User.userID)
                .join(UserProfile, User.userID == UserProfile.user_id)
                .join(Category, cls.categoryID == Category.categoryID)
                .filter(cls.serviceStatus == True)
                .filter(User.isActive == True)
                .filter(Category.categoryStatus == True)
                .filter(
                    or_(
                        cls.title.ilike(f'%{keyword}%'),
                        cls.description.ilike(f'%{keyword}%'),
                        Category.name.ilike(f'%{keyword}%'),
                        UserProfile.first_name.ilike(f'%{keyword}%'),
                        UserProfile.last_name.ilike(f'%{keyword}%')
                    )
                )
                .all()
            )
            
            return results
        except Exception as e:
            print(f"Error searching services: {str(e)}")
            return []
    
    @classmethod
    def search_by_keyword(cls, cleaner_id, keyword):
        """
        Search for cleaning services by keyword for a specific cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
            keyword (str): Search keyword
        
        Returns:
            list: List of services matching the search criteria
        """
        if not keyword or not keyword.strip():
            # If no keyword provided, return all services for this cleaner
            return cls.find_by_cleaner(cleaner_id)
        
        try:
            # Search for services that match the keyword in title or description
            # and belong to the specified cleaner
            return (cls.query
                  .filter(
                      cls.cleanerID == cleaner_id,
                      or_(
                          cls.title.ilike(f'%{keyword}%'),
                          cls.description.ilike(f'%{keyword}%')
                      )
                  ).all())
        except Exception:
            # Return empty list in case of error
            return []
    
    @classmethod
    def get_shortlist_count(cls, service_id):
        """
        Get the number of times a service has been shortlisted
        
        Args:
            service_id (int): ID of the service
        
        Returns:
            int: Count of shortlists for this service
        """
        from entity.Shortlist import Shortlist
        return Shortlist.query.filter_by(serviceID=service_id).count()
        
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
        
    def suspend(self):
        """Suspend a category by setting serviceStatus to False"""
        self.serviceStatus = False
        db.session.commit()
        return True

    def reactivate(self):
        """Reactivate a category by setting serviceStatus to True"""
        self.serviceStatus = True
        db.session.commit()
        return True