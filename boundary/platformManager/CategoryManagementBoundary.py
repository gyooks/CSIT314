from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.platformManager.viewCategoryController import viewCategoryController

# Create Platform Manager Category Blueprint
platformManager_category_bp = Blueprint('platformManager_category', __name__, url_prefix='/platform_manager')

# Category Management View
@platformManager_category_bp.route('/categories')
def manage_categories():
    """
    Display all categories
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('platformManager_login.platformManagerLogin'))
    user_id = session['user_id']
    
    # Get all categories
    categories = viewCategoryController.get_all_categories()
    return render_template('platformManager/categoryManagementPage.html', categories=categories)

# Create New Category - GET
@platformManager_category_bp.route('/categories/create', methods=['GET'])
def create_category_form():
    """
    Show category creation form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    user_id = session['user_id']

    return render_template('platformManager/createCategory.html')

# Create New Category - POST
@platformManager_category_bp.route('/categories/create', methods=['POST'])
def create_category():
    """
    Process category creation form
    """
    # if 'user_id' not in session:
    #     flash("You must be logged in to perform this action", "danger")
    #     return redirect(url_for('platform_manager_login.userManagerLogin'))
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    status = request.form.get('categoryStatus')
    
    # Validate form data
    if not name:
        flash("Category name is required", "danger")
        return redirect(url_for('platformManager_category.create_category_form'))

    # Create category 
    success, message = viewCategoryController.create_category(name, description, status)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('platformManager_category.manage_categories'))

# Edit Category - GET
@platformManager_category_bp.route('/categories/edit/<int:category_id>', methods=['GET'])
def edit_category_form(category_id):
    """
    Show category edit form
    """
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    user_id = session['user_id']

    # Get category by ID
    category = viewCategoryController.get_category_by_id(category_id)
    
    if not category:
        flash("Category not found.", "danger")
        return redirect(url_for('platformManager_category.manage_categories'))
    
    return render_template('platformManager/editCategory.html', category=category)

# Edit Category - POST
@platformManager_category_bp.route('/categories/edit/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    """
    Process category edit form
    """
    # if 'user_id' not in session:
    #     flash("You must be logged in to perform this action", "danger")
    #     return redirect(url_for('platform_manager_login.userManagerLogin'))
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    status = request.form.get('categoryStatus')
    
    # Validate form data
    if not name:
        flash("Category name is required", "danger")
        return redirect(url_for('platformManager_category.edit_category_form', category_id=category_id))
    
    # Update category
    success = viewCategoryController.update_category(category_id, name, description, status)
    
    if success:
        flash("Category updated successfully!", "success")
    else:
        flash("Failed to update category.", "danger")
    
    return redirect(url_for('platformManager_category.manage_categories'))

# Delete Category
@platformManager_category_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """
    Delete a category
    """
    # if 'user_id' not in session:
    #     flash("You must be logged in to perform this action", "danger")
    #     return redirect(url_for('platform_manager_login.userManagerLogin'))
    
    # Delete category
    success = viewCategoryController.delete_category(category_id)
    
    if success:
        flash("Category deleted successfully.", "success")
    else:
        flash("Failed to delete category.", "danger")
    
    return redirect(url_for('platformManager_category.manage_categories'))



@platformManager_category_bp.route('/categories/suspend/<int:category_id>', methods=['POST'])
def suspend_category(category_id):
    # This would typically have authentication checks to ensure only admins can access
    # if 'user_id' not in session:
    #     flash("You must be logged in to perform this action", "danger")
    #     return redirect(url_for('admin_login.userAdminLogin'))
    
    # Call controller to suspend the category
    success, message = viewCategoryController.suspend_category(category_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    # Redirect back to the categories page with fresh data
    return redirect(url_for('platformManager_category.manage_categories'))

@platformManager_category_bp.route('/categories/reactivate/<int:category_id>', methods=['POST'])
def reactivate_category(category_id):
    # This would typically have authentication checks to ensure only admins can access
    
    # Call controller to reactivate the category
    success, message = viewCategoryController.reactivate_category(category_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    # Redirect back to the categories page with fresh data
    return redirect(url_for('platformManager_category.manage_categories'))

# Search Categories
@platformManager_category_bp.route('/categories/search', methods=['POST'])
def search_category():
    """
    Search categories by keyword
    """
    # if 'user_id' not in session:
    #     flash("You must be logged in to perform this action", "danger")
    #     return redirect(url_for('platform_manager_login.userManagerLogin'))
    
    # Get search keyword
    keyword = request.form.get('keyword', '')
    
    # Search categories
    categories = viewCategoryController.search_categories(keyword)
    
    return render_template('platformManager/categoryManagementPage.html', 
                         categories=categories, 
                         search_keyword=keyword)