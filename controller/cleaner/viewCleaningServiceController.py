from entity.CleaningService import CleaningService
from entity.Category import Category

class ViewCleaningServiceController:
    """
    Controller for viewing cleaning services
    """
    
    def get_cleaner_services(self, cleaner_id):
        """
        Get all cleaning services for a specific cleaner
        
        Args:
            cleaner_id (int): ID of the cleaner
        
        Returns:
            list: List of cleaning service objects
        """
        return CleaningService.find_by_cleaner(cleaner_id)
    
    def get_service_by_id(self, service_id):
        """
        Get a specific cleaning service by ID
        
        Args:
            service_id (int): ID of the service
        
        Returns:
            CleaningService: The cleaning service object
        """
        return CleaningService.find_by_id(service_id)
    
    def get_services_by_category(self, category_id):
        """
        Get all cleaning services in a specific category
        
        Args:
            category_id (int): ID of the category
        
        Returns:
            list: List of cleaning service objects
        """
        return CleaningService.find_by_category(category_id)
    
    def get_service_with_category_details(self, service_id):
        """
        Get a cleaning service with its category details
        
        Args:
            service_id (int): ID of the service
        
        Returns:
            dict: Service and category details
        """
        service = CleaningService.find_by_id(service_id)
        if not service:
            return None
        
        category = Category.find_by_id(service.categoryID)
        
        service_dict = service.to_dict()
        service_dict['category_name'] = category.name if category else 'Unknown'
        
        return service_dict
    
    def get_cleaner_services_with_shortlist_count(self, cleaner_id):
        """
        Get all cleaning services for a specific cleaner with shortlist counts
        
        Args:
            cleaner_id (int): ID of the cleaner
        
        Returns:
            list: List of cleaning service objects with shortlist count
        """
        services = self.get_cleaner_services(cleaner_id)
        
        # Enhance each service with shortlist count
        for service in services:
            service.shortlist_count = CleaningService.get_shortlist_count(service.serviceID)
        
        return services

# Create an instance of the controller
viewCleaningServiceController = ViewCleaningServiceController()


