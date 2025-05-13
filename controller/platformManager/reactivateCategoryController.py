from entity.Category import Category
from db_config import db

@staticmethod
def reactivate_category(category_id):
        """
        Reactivate a suspended category by setting categoryStatus to True
        """
        try:
            # Find category by ID
            category = Category.find_by_id(category_id)
            
            if not category:
                return False, "Category not found"
            
            # Set categoryStatus to True (reactivated)
            category.reactivate()
            
            return True, "Category reactivated successfully"
        
        except Exception as e:
            db.session.rollback()
            return False, f"Error reactivating category: {str(e)}"