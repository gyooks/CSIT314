from entity.Category import Category
from db_config import db

class updateCategoryController:
    @staticmethod
    def update_category(category_id, name=None, description=None, status=None):
        """
        Get category and update information if data is provided
        """
        try:
            # Find the category
            category = Category.find_by_id(category_id)
            
            if not category:
                return False, "Category not found", None
                
            # If no update data is provided, just return the category (for GET requests)
            if all(param is None for param in [name, description, status]):
                return True, "Category retrieved", category.to_dict()
                
            # Update category if data is provided
            if any(param is not None for param in [name, description, status]):
                # Use existing status if not provided
                category_status = status if status is not None else category.categoryStatus
                
                category.update_in_db(name, description, category_status)
                return True, "Category updated successfully", category.to_dict()
                
        except Exception as e:
            print(f"Error handling category: {e}")
            db.session.rollback()
            return False, f"Error: {str(e)}", None