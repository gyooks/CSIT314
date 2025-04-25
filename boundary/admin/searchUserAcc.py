from flask import Blueprint, render_template, request
from controller.admin.searchUserAccController import SearchUserController

search_user_bp = Blueprint('search_user', __name__, url_prefix='/search')
controller = SearchUserController()

@search_user_bp.route('/', methods=['GET', 'POST'])
def search_user():
    keyword = ""
    results = []
    users = []
    
    if request.method == 'POST':
        keyword = request.form['keyword']
        search_results = controller.search_user(keyword)
        
        # Format the results to match what the dashboard template expects
        for user, profile in search_results:
            users.append(user)
    
    return render_template('admin/dashboard.html', users=users, search_keyword=keyword)

