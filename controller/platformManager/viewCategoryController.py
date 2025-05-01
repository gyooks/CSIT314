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
    
    @staticmethod
    def create_category(name, description, status):
        """
        Create a new category, ensuring no duplicate names
        """
        try:
            # Check for duplicates using the model method
            if Category.find_by_name(name):
                return False, "Category name already exists"

            # Convert status string to boolean
            category_status = (status == '1')

            # Create and save the new category
            category = Category(name=name, description=description, categoryStatus=category_status)
            category.save_to_db()
            return True, "Category created successfully"
        except Exception as e:
            print(f"Error creating category: {e}")
            db.session.rollback()
            return False, "Error creating category"

    
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
    
    @staticmethod
    def search_categories(keyword):
        """
        Search categories by keyword
        """
        try:
            categories = Category.search_by_keyword(keyword)
            return [category.to_dict() for category in categories]
        except Exception as e:
            print(f"Error searching categories: {e}")
            return []