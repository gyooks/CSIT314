from entity.CleaningService import CleaningService
from entity.Category import Category

class UpdateCleaningServiceController:

    def update_service(self, service_id, title, description, price, category_id):
        """
        Get a service by ID and update it with new values
            
        Returns:
            tuple: (bool, CleaningService or None) - Success status and the service object
                   The service object is returned even if update fails to allow for error handling
        """
        # Get the service
        service = CleaningService.find_by_id(service_id)
        if not service:
            return False, None
            
        # Validate inputs
        if not title or not title.strip():
            return False, service
            
        try:
            # Convert price to float
            price = float(price)
            if price <= 0:
                return False, service
        except ValueError:
            return False, service
            
        # Check if category exists and is active
        category = Category.find_by_id(category_id)
        if not category or not category.categoryStatus:
            return False, service
            
        try:
            # Update the service
            update_success = service.update_service(title, description, price, category_id)
            return update_success, service
        except Exception:
            return False, service

# Create an instance of the controller
updateCleaningServiceController = UpdateCleaningServiceController()