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

    def create_booking(self, homeowner_id, service_id, booking_date, hours):
        """
        Create a new booking for a service
        
        Args:
            homeowner_id (int): ID of the homeowner
            service_id (int): ID of the service
            booking_date (str): Date of the booking in YYYY-MM-DD format
            hours (int): Number of hours for the booking
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Convert hours to integer
            hours = int(hours)
            
            # Check if service exists and is active
            service = CleaningService.find_by_id(service_id)
            if not service or not service.serviceStatus:
                return False, "Service not found or unavailable"
            
            # Check if date is valid
            try:
                booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
                if booking_date_obj < datetime.now().date():
                    return False, "Booking date cannot be in the past"
            except ValueError:
                return False, "Invalid date format. Please use YYYY-MM-DD format"
            
            # Get cleaner ID from service
            cleaner_id = service.cleanerID
            
            # Check if cleaner is active
            cleaner = User.find_by_id(cleaner_id)
            if not cleaner or not cleaner.isActive:
                return False, "Cleaner is not available"
            
            # Calculate total price
            total_price = service.price * hours
            
            # Create new booking with default status 'Pending'
            Booking.create_new_booking(
                homeowner_id=homeowner_id,
                service_id=service_id,
                cleaner_id=cleaner_id,
                booking_date=booking_date_obj,
                hours=hours,
                total_price=total_price
            )
            
            return True, "Booking created successfully. Waiting for cleaner confirmation."
        except Exception as e:
            from db_config import db
            db.session.rollback()
            print(f"Error creating booking: {str(e)}")
            return False, "An error occurred while creating your booking"
    
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