from entity.CleaningService import CleaningService
from entity.Shortlist import Shortlist

class searchServiceController:
    def search_services(self, keyword):
        """
        Search active cleaning services by keyword with cleaner info
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (service, cleaner, cleaner_profile, category)
        """
        return CleaningService.search_services_with_details(keyword)