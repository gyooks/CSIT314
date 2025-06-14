from entity.Category import Category
from db_config import db

class suspendCategoryController:
    @staticmethod
    def suspend_category(category_id):
        """
        Suspend a category by setting status to False
        """
        try:
            # Find category by ID
            category = Category.find_by_id(category_id)
            
            if not category:
                return False, "Category not found"
            
            # Set status to False (suspended)
            category.suspend()
            
            return True, "Category suspended successfully"
        
        except Exception as e:
            db.session.rollback()
            return False, f"Error suspending category: {str(e)}"

    
    