from entity.Booking import Booking
from entity.CleaningService import CleaningService
from entity.UserAccount import User
from datetime import datetime

class viewBookingHistoryController:
    @staticmethod
    def get_all_bookings(homeowner_id):
        """
        Get all bookings for a homeowner
        
        Args:
            homeowner_id (int): ID of the homeowner
            
        Returns:
            list: List of tuples containing (booking, cleaner, cleaner_profile, service)
        """
        return Booking.get_homeowner_bookings_with_details(homeowner_id)
        
    @staticmethod
    def get_bookings_by_status(homeowner_id, status):
        """
        Get bookings for a homeowner filtered by status
        
        Args:
            homeowner_id (int): ID of the homeowner
            status (str): Booking status to filter by
            
        Returns:
            list: List of tuples containing (booking, cleaner, cleaner_profile, service)
        """
        return Booking.get_homeowner_bookings_with_details(homeowner_id, status)
    

