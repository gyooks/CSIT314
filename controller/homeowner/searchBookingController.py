from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from datetime import datetime

def search_bookings(self, homeowner_id, keyword):
        """
        Search bookings for a homeowner by keyword
        
        Args:
            homeowner_id (int): ID of the homeowner
            keyword (str): Search keyword
            
        Returns:
            list: List of tuples containing (booking, cleaner, cleaner_profile, service)
        """
        return Booking.search_homeowner_bookings(homeowner_id, keyword)
