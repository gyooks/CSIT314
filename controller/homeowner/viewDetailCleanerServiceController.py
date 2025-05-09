from entity.CleaningService import CleaningService

class ViewDetailCleanerServiceController:
    def get_service_detail(self, service_id):
        """
        Get detailed information about a specific cleaning service
        
        Args:
            service_id (int): ID of the service to retrieve
            
        Returns:
            tuple: Tuple containing (service, cleaner, category) or None if not found
        """
        try:
            # Get service details with related cleaner and category information
            service_details = CleaningService.get_service_detail_with_relations(service_id)
            
            if service_details:
                return service_details
            else:
                return None
        except Exception as e:
            print(f"Error getting service details: {str(e)}")
            return None

# Create controller instance
viewDetailCleanerServiceController = ViewDetailCleanerServiceController()