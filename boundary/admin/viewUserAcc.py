from flask import Blueprint, render_template
from controller.admin.viewUserAccController import viewUserAccController

# Create Admin Dashboard Blueprint
admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route('/dashboard')
def dashboard():
    # This would typically have authentication checks
    users = viewUserAccController.get_all_users()
    return render_template('admin/dashboard.html', users=users)