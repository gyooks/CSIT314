from flask import Blueprint, render_template, request
from controller.admin.searchUserAccController import SearchUserController

search_user_bp = Blueprint('search_user', __name__, url_prefix='/search')
controller = SearchUserController()

@search_user_bp.route('/', methods=['GET', 'POST'])
def search_user():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = controller.search_user(keyword)
    return render_template('admin/searchUserAcc.html', results=results)
