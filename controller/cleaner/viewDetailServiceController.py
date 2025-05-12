from entity.CleaningService import CleaningService
from entity.Category import Category
from entity.UserAccount import User
from entity.Shortlist import Shortlist

class ViewDetailServiceController:
    def get_service_detail(self, service_id, cleaner_id):
        """
        Get detailed information for a specific cleaning service,
        with verification that it belongs to the specified cleaner.
            
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
        
        # Get recent shortlist users (limited to 10)
        try:
            # Retrieve recent shortlists with user information
            shortlists = Shortlist.get_recent_by_service(service_id, limit=10)
            
            # Format shortlist data
            recent_shortlists = []
            for shortlist in shortlists:
                user = User.find_by_id(shortlist.homeownerID)
                
                recent_shortlists.append({
                    'shortlist_id': shortlist.shortlistID,
                    'homeowner_id': shortlist.homeownerID,
                    'homeowner_name': f"{user.first_name} {user.last_name}" if user else "Unknown User",
                    'created_at': shortlist.create_at
                })
        except Exception as e:
            print(f"Error retrieving shortlists: {str(e)}")
            recent_shortlists = []
        
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

# Create an instance of the controller
viewDetailServiceController = ViewDetailServiceController()