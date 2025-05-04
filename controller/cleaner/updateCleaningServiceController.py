from entity.CleaningService import CleaningService
from entity.Category import Category

class UpdateCleaningServiceController:
    """
    Controller for updating cleaning services
    """
    
    def get_service_by_id(self, service_id):
        """
        Get a specific cleaning service by ID
        
        Args:
            service_id (int): ID of the service
        
        Returns:
            CleaningService: The cleaning service object
        """
        return CleaningService.find_by_id(service_id)
    
    def update_service(self, service_id, title, description, price, category_id):
        """
        Update an existing cleaning service
        
        Args:
            service_id (int): ID of the service to update
            title (str): Updated title of the service
            description (str): Updated description of the service
            price (float): Updated price of the service
            category_id (int): Updated category ID
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        # Get the service
        service = CleaningService.find_by_id(service_id)
        if not service:
            return False
        
        # Validate inputs
        if not title or not title.strip():
            return False
        
        try:
            # Convert price to float
            price = float(price)
            if price <= 0:
                return False
        except ValueError:
            return False
        
        # Check if category exists and is active
        category = Category.find_by_id(category_id)
        if not category:
            return False
        
        if not category.categoryStatus:
            return False
        
        try:
            # Update the service
            return service.update_service(title, description, price, category_id)
        except Exception:
            return False

# Create an instance of the controller
updateCleaningServiceController = UpdateCleaningServiceController()