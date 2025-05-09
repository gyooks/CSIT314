from entity.Shortlist import Shortlist
from entity.CleaningService import CleaningService
from entity.Category import Category

class ShortlistServiceController:
    def add_to_shortlist(self, homeowner_id, service_id):
        """
        Add a service to the homeowner's shortlist
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            tuple: (success, message)
        """

        # Check if service exists and is active
        service = CleaningService.find_by_id(service_id)
        if not service or not service.serviceStatus:
            return False, "Service not found or unavailable"  
        
        # Check if service is already shortlisted
        existing_shortlist = Shortlist.find_existing_shortlist(homeowner_id, service_id)
        if existing_shortlist:
            return False, "This service is already in your shortlist"
        
        # Add service to shortlist
        success = Shortlist.add_service(homeowner_id, service_id)
        if success:
            return True, "Service added to your shortlist"
        else:
            return False, "An error occurred while adding to shortlist"
    
    def remove_from_shortlist(self, homeowner_id, service_id):
        """
        Remove a service from the homeowner's shortlist
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            tuple: (success, message)
        """
        # Find shortlist entry
        shortlist = Shortlist.find_existing_shortlist(homeowner_id, service_id)
        if not shortlist:
            return False, "This service is not in your shortlist"
        
        # Remove from shortlist
        success = Shortlist.remove_service(shortlist)
        if success:
            return True, "Service removed from your shortlist"
        else:
            return False, "An error occurred while removing from shortlist"
    
    def get_homeowner_shortlist(self, homeowner_id):
        """
        Get all shortlisted services for a homeowner with service and cleaner info
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of tuples containing (shortlist, service, cleaner, cleaner_profile, category)
        """
        results = Shortlist.get_homeowner_shortlist(homeowner_id)
        
        # If empty, could add a message here if needed
        return results

    def search_shortlist(self, homeowner_id, keyword):
        """
        Search through homeowner's shortlisted services
        
        Args:
            homeowner_id (int): ID of the homeowner
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (shortlist, service, cleaner, cleaner_profile, category)
        """
        if not keyword or keyword.strip() == "":
            # If keyword is empty, return all shortlisted services
            return self.get_homeowner_shortlist(homeowner_id)
        
        # Search in shortlisted services
        results = Shortlist.search_homeowner_shortlist(homeowner_id, keyword)
        return results

# Create controller instance
shortlistServiceController = ShortlistServiceController()