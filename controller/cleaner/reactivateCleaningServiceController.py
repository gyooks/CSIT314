from entity.CleaningService import CleaningService

class reactivateCleaningServiceController:
     
    def reactivate_service(self, service_id):
        """
        Reactivate a suspended cleaning service
        
        Args:
            service_id (int): ID of the service to reactivate
        
        Returns:
            tuple: (success, message)
        """
        # Get the service
        service = CleaningService.find_by_id(service_id)
        if not service:
            return False, "Service not found"
        
        if service.serviceStatus:
            return False, "Service is already active"
        
        try:
            # Reactivate the service
            if service.reactivate():
                return True, "Service has been activated successfully"
            else:
                return False, "Failed to activate service"
        except Exception as e:
            return False, f"Error activating service: {str(e)}"