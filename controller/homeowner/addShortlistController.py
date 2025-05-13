from entity.Shortlist import Shortlist
from entity.CleaningService import CleaningService
from entity.Category import Category

class addShortlistController:
    @staticmethod
    def add_to_shortlist(homeowner_id, service_id):
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