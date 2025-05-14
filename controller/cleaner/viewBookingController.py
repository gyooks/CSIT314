from entity.Booking import Booking

class ViewBookingController:
    """
    Controller for viewing and managing bookings
    """

    
    def get_cleaner_bookings_with_details(self, cleaner_id):
        """
        Get all bookings for a specific cleaner with homeowner and service details
        
        Args:
            cleaner_id (int): ID of the cleaner
            
        Returns:
            list: List of bookings with associated details
        """
        return Booking.get_bookings_by_cleaner_with_details(cleaner_id)
    

 
