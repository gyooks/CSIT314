from entity.Category import Category
from db_config import db

class createCategoryController:
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
