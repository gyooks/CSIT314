from entity.CleaningService import CleaningService
from entity.Category import Category

class ViewCleaningServiceController:
    """
    Controller for viewing cleaning services
    """
    
    def get_cleaner_services(self, cleaner_id):
        """
        Get all cleaning services for a specific cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
        
        Returns:
            list: List of cleaning service objects
        """
        return CleaningService.find_by_cleaner(cleaner_id)
   


# Create an instance of the controller
viewCleaningServiceController = ViewCleaningServiceController()