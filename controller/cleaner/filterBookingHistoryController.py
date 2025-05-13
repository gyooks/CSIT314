from entity.Booking import Booking

class filterBookingHistoryController:

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