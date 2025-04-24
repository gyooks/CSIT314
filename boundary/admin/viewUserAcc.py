from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.admin.viewUserAccController import viewUserAccController

# Create Admin Dashboard Blueprint
admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route('/dashboard')
def dashboard():
    # This would typically have authentication checks
    users = viewUserAccController.get_all_users()
    return render_template('admin/dashboard.html', users=users)

@admin_dashboard_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    success = viewUserAccController.delete_user(user_id)
    if success:
        flash('User deleted successfully.', 'success')
    else:
        flash('User could not be deleted.', 'danger')
    return redirect(url_for('admin_dashboard.dashboard'))