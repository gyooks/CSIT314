from flask import Blueprint, redirect, url_for, flash, request, session
from controller.admin.suspendUserAccController import suspendUserAccController

# Suspend User Account Blueprint
suspend_user_bp = Blueprint('suspend_user', __name__, url_prefix='/admin')

@suspend_user_bp.route('/suspend_user/<int:target_user_id>', methods=['POST'])
def suspend_user(target_user_id):
    # This would typically have authentication checks to ensure only admins can access
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    
    # Call controller to suspend the user
    success, message = suspendUserAccController.suspend_user(target_user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    # Redirect back to the admin dashboard
    return redirect(url_for('admin_dashboard.dashboard'))

@suspend_user_bp.route('/reactivate_user/<int:target_user_id>', methods=['POST'])
def reactivate_user(target_user_id):
    # This would typically have authentication checks to ensure only admins can access
    
    # Call controller to reactivate the user
    success, message = suspendUserAccController.reactivate_user(target_user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    # Redirect back to the admin dashboard
    return redirect(url_for('admin_dashboard.dashboard'))