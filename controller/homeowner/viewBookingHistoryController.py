from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from datetime import datetime    
    
class Gethomeownerbookings:
    def get_homeowner_bookings(self, homeowner_id, status=None):
            """
            Get all bookings for a homeowner with optional status filter
            
            Args:
                homeowner_id (int): ID of the homeowner
                status (str, optional): Filter by booking status
                
            Returns:
                list: List of tuples containing (booking, cleaner, cleaner_profile, service)
            """
            return Booking.get_homeowner_bookings_with_details(homeowner_id, status)