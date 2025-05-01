from entity.Category import Category
from db_config import db

class viewCategoryController:
    @staticmethod
    def get_all_categories():
        """
        Get all categories from database
        """
        try:
            categories = Category.get_all()
            return [category.to_dict() for category in categories]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Get category by ID
        """
        try:
            category = Category.find_by_id(category_id)
            if category:
                return category.to_dict()
            return None
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    

   
