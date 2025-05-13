from entity.Category import Category
from db_config import db

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
    