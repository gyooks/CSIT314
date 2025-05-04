from entity.CleaningService import CleaningService

class DeleteCleaningServiceController:
    """
    Controller for deleting cleaning services
    """
    
    def delete_service(self, service_id):
        """
        Delete a cleaning service
        
        Args:
            service_id (int): ID of the service to delete
        
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        # Get the service
        service = CleaningService.find_by_id(service_id)
        if not service:
            return False
        
        try:
            # Delete the service
            service.delete_from_db()
            return True
        except Exception:
            return False

# Create an instance of the controller
deleteCleaningServiceController = DeleteCleaningServiceController()