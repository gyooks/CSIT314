from entity.Shortlist import Shortlist
from entity.CleaningService import CleaningService
from entity.Category import Category

class viewShortlistController:
    @staticmethod  
    def get_homeowner_shortlist(homeowner_id):
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