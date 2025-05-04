from entity.CleaningService import CleaningService

class SearchCleaningServiceController:
    """
    Controller for searching cleaning services
    """
    
    def search_services(self, cleaner_id, keyword):
        """
        Search for cleaning services by keyword for a specific cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
            keyword (str): Search keyword
        
        Returns:
            list: List of services matching the search criteria
        """
        # Use the search method from the entity model
        return CleaningService.search_by_keyword(cleaner_id, keyword)

# Create an instance of the controller
searchCleaningServiceController = SearchCleaningServiceController()