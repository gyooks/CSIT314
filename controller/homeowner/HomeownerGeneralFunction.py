from entity.Shortlist import Shortlist
from entity.CleaningService import CleaningService
from entity.Category import Category

class HomeownerGeneralFunction:
    @staticmethod
    def remove_from_shortlist(homeowner_id, service_id):
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
    
    
