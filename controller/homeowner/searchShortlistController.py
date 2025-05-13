from entity.Shortlist import Shortlist
from entity.CleaningService import CleaningService
from entity.Category import Category

class SearchShortlistController:
    @staticmethod
    def search_shortlist(homeowner_id, keyword):
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
