from entity.Category import Category
from db_config import db

class updateCategoryController:
    @staticmethod
    def update_category(category_id, name, description, status):
        """
        Update category attributes
        """
        try:
            category = Category.find_by_id(category_id)
            if not category:
                return False
                
            # Convert status string to boolean
            category_status = (status == '1')
            
            category.update_in_db(name, description, category_status)
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            db.session.rollback()
            return False