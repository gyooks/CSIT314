from entity.CleaningService import CleaningService
from entity.Category import Category

class CreateCleaningServiceController:
    """
    Controller for creating cleaning services
    """
    
    def create_service(self, cleaner_id, category_id, title, description, price):
        """
        Create a new cleaning service
        
        Args:
            cleaner_id (int): ID of the cleaner
            category_id (int): ID of the category
            title (str): Title of the service
            description (str): Description of the service
            price (float): Price of the service
        
        Returns:
            tuple: (success, message)
        """
        # Validate inputs
        if not title or not title.strip():
            return False, "Service title is required"
        
        try:
            # Convert price to float
            price = float(price)
            if price <= 0:
                return False, "Price must be greater than zero"
        except ValueError:
            return False, "Invalid price format"
        
        # Check if category exists and is active
        category = Category.find_by_id(category_id)
        if not category:
            return False, "Category not found"
        
        if not category.categoryStatus:
            return False, "Selected category is not active"
        
        # Create the service
        try:
            service = CleaningService(
                cleanerID=cleaner_id,
                categoryID=category_id,
                title=title,
                description=description,
                price=price
            )
            service.save_to_db()
            return True, "Cleaning service created successfully"
        except Exception as e:
            return False, f"Error creating service: {str(e)}"

# Create an instance of the controller
createCleaningServiceController = CreateCleaningServiceController()