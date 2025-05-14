from entity.Booking import Booking

class cleanerGeneralFunction:
          
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


    def get_booking_by_id(self, booking_id):
        """
        Get a specific booking by ID
        
        Args:
            booking_id (int): ID of the booking
            
        Returns:
            Booking: Booking object
        """
        return Booking.find_by_id(booking_id)

# Create an instance of the controller
cleanerGeneralFunction = cleanerGeneralFunction()