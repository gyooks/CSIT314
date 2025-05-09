from entity.CleaningService import CleaningService
from entity.Category import Category
from entity.UserAccount import User
from entity.Shortlist import Shortlist

class ViewDetailServiceController:
    """
    Controller for viewing detailed cleaning service information
    """
    
    def get_service_detail(self, service_id, cleaner_id):
        """
        Get detailed information for a specific cleaning service,
        with verification that it belongs to the specified cleaner.
        
        Args:
            service_id (int): ID of the service to view
            cleaner_id (int): ID of the cleaner requesting to view the service
        
        Returns:
            dict: Detailed service information including related stats and data,
                  or None if service not found or not owned by this cleaner
        """
        # Get basic service information
        service = CleaningService.find_by_id(service_id)
        
        # Check if service exists and belongs to this cleaner
        if not service or service.cleanerID != cleaner_id:
            return None
        
        # Get category information
        category = Category.find_by_id(service.categoryID)
        
        # Get shortlist information
        shortlist_count = CleaningService.get_shortlist_count(service_id)
        
        # Get recent shortlist users (limited to 5)
        recent_shortlists = self.get_recent_shortlists(service_id)
        
        # Create a comprehensive service detail dictionary
        service_detail = {
            # Basic service info
            'serviceID': service.serviceID,
            'title': service.title,
            'description': service.description,
            'price': float(service.price) if service.price else None,
            'status': service.serviceStatus,
            'created_at': service.create_at,
            
            # Category info
            'category_name': category.name if category else 'Unknown Category',
            'category_id': service.categoryID,
            
            # Stats
            'shortlist_count': shortlist_count,
            'recent_shortlists': recent_shortlists,
            
            # Make the service object available too for convenience
            'service_obj': service
        }
        
        return service_detail
    
    def get_recent_shortlists(self, service_id, limit=5):
        """
        Get recent shortlists for a specific service
        
        Args:
            service_id (int): ID of the service
            limit (int): Maximum number of shortlists to return
        
        Returns:
            list: List of recent shortlists with user information
        """
        try:
            # Retrieve recent shortlists with user information
            shortlists = Shortlist.get_recent_by_service(service_id, limit)
            
            # Format shortlist data
            shortlist_data = []
            for shortlist in shortlists:
                user = User.find_by_id(shortlist.homeownerID)
                
                shortlist_data.append({
                    'shortlist_id': shortlist.shortlistID,
                    'homeowner_id': shortlist.homeownerID,
                    'homeowner_name': f"{user.first_name} {user.last_name}" if user else "Unknown User",
                    'created_at': shortlist.create_at
                })
            
            return shortlist_data
            
        except Exception as e:
            print(f"Error retrieving shortlists: {str(e)}")
            return []

# Create an instance of the controller
viewDetailServiceController = ViewDetailServiceController()