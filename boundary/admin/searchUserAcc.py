from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from controller.admin.searchUserAccController import SearchUserAccController

search_userAcc_bp = Blueprint('search_userAcc', __name__, url_prefix='/search')
controller = SearchUserAccController()

@search_userAcc_bp.route('/', methods=['GET', 'POST'])
def search_userAcc():
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
        
    keyword = ""
    results = []
    users = []
    
    # Check if it's a POST request (search form submitted)
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            # Get search results from controller
            results = controller.search_userAcc(keyword)
            
            # Process results to get the user objects only
            users = [user for user, _ in results]
    
    # Render the template with search results
    return render_template('admin/dashboard.html', 
                          users=users, 
                          search_keyword=keyword)