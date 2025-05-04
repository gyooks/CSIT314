from entity.Booking import Booking

class ViewBookingController:
    """
    Controller for viewing and managing bookings
    """
    
    def get_cleaner_bookings(self, cleaner_id):
        """
        Get all bookings for a specific cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
            
        Returns:
            list: List of booking objects
        """
        return Booking.get_bookings_by_cleaner(cleaner_id)
    
    def get_cleaner_bookings_with_details(self, cleaner_id):
        """
        Get all bookings for a specific cleaner with homeowner and service details
        
        Args:
            cleaner_id (int): ID of the cleaner
            
        Returns:
            list: List of bookings with associated details
        """
        return Booking.get_bookings_by_cleaner_with_details(cleaner_id)
    
    def get_booking_by_id(self, booking_id):
        """
        Get a specific booking by ID
        
        Args:
            booking_id (int): ID of the booking
            
        Returns:
            Booking: Booking object
        """
        return Booking.find_by_id(booking_id)
    
    def update_booking_status(self, booking_id, new_status):
        """
        Update the status of a booking
        
        Args:
            booking_id (int): ID of the booking
            new_status (str): New status for the booking
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        booking = self.get_booking_by_id(booking_id)
        if booking:
            return booking.update_status(new_status)
        return False
    
    def filter_bookings_by_status(self, cleaner_id, status):
        """
        Filter bookings by status for a cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
            status (str): Status to filter by
            
        Returns:
            list: List of filtered bookings with details
        """
        return Booking.filter_bookings_by_status_with_details(cleaner_id, status)