from entity.Category import Category
from db_config import db

class deleteCategoryController:
    @staticmethod
    def delete_category(category_id):
        """
        Delete a category
        """
        try:
            category = Category.find_by_id(category_id)
            if category:
                category.delete_from_db()
                return True
            return False
        except Exception as e:
            print(f"Error deleting category: {e}")
            db.session.rollback()
            return False