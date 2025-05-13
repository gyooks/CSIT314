from entity.CleaningService import CleaningService

class SuspendCleaningServiceController:
    """
    Controller for suspending and reactivating cleaning services
    """
    
    def suspend_service(self, service_id):
        """
        Suspend a cleaning service
        
        Args:
            service_id (int): ID of the service to suspend
        
        Returns:
            tuple: (success, message)
        """
        # Get the service
        service = CleaningService.find_by_id(service_id)
        if not service:
            return False, "Service not found"
        
        if not service.serviceStatus:
            return False, "Service is already inactive"
        
        try:
            # Suspend the service
            if service.suspend():
                return True, "Service has been deactivated successfully"
            else:
                return False, "Failed to deactivate service"
        except Exception as e:
            return False, f"Error deactivating service: {str(e)}"
    
   

# Create an instance of the controller
suspendCleaningServiceController = SuspendCleaningServiceController()