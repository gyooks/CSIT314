from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from datetime import datetime

class BookingServiceController:
    
    def get_all_bookings(self, homeowner_id):
        """
        Get all bookings for a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of tuples containing (booking, cleaner, cleaner_profile, service)
        """
        return Booking.get_homeowner_bookings_with_details(homeowner_id)
    
    def get_bookings_by_status(self, homeowner_id, status):
        """
        Get bookings for a homeowner filtered by status
        
        Args:
            homeowner_id (int): ID of the homeowner
            status (str): Booking status to filter by
            
        Returns:
            list: List of tuples containing (booking, cleaner, cleaner_profile, service)
        """
        return Booking.get_homeowner_bookings_with_details(homeowner_id, status)
    
    

    
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
    

# Create controller instance
BookingServiceController = BookingServiceController()