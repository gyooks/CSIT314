from entity.CleaningService import CleaningService
from entity.Shortlist import Shortlist

class ViewCleanerServiceController:
    def get_all_services(self):
        """
        Get all active cleaning services with cleaner info for homeowner view
        
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        return CleaningService.get_all_services_with_details()
    
    def get_services_by_category(self, category_id):
        """
        Get active cleaning services filtered by category with cleaner info
        
        Args:
            category_id (int): ID of the category to filter by
            
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        return CleaningService.get_services_by_category_with_details(category_id)
    

    def get_shortlisted_service_ids(self, homeowner_id):
        """
        Get list of service IDs shortlisted by a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of shortlisted service IDs
        """
        return Shortlist.get_shortlisted_service_ids(homeowner_id)
    
    def is_service_shortlisted(self, homeowner_id, service_id):
        """
        Check if a service is shortlisted by a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            
        Returns:
            bool: True if service is shortlisted, False otherwise
        """
        return Shortlist.is_service_shortlisted(homeowner_id, service_id)



# Create controller instance
viewCleanerServiceController = ViewCleanerServiceController()