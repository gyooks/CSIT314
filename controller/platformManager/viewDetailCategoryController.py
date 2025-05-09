from entity.Category import Category
from db_config import db

class viewDetailCategoryController:
    @staticmethod
    def get_category_detail(category_id):
        """
        Get detailed information about a specific category
        
        Args:
            category_id (int): The ID of the category to retrieve
            
        Returns:
            dict: Category details including ID, name, description, status, and creation date
                  Returns None if category not found
        """
        try:
            # Get category by ID from entity layer
            category = Category.find_by_id(category_id)
            
            if not category:
                return None
                
            # Additional data could be retrieved here, such as:
            # - Count of services using this category
            # - Related statistics or metrics
            
            # Convert category object to dictionary with all details
            category_detail = category.to_dict()

            
            return category_detail
            
        except Exception as e:
            print(f"Error getting category details: {e}")
            return None