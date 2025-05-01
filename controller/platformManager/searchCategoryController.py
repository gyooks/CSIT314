from entity.Category import Category
from db_config import db

class searchCategoryController:
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