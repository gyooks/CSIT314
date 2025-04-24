from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.admin.viewUserAccController import viewUserAccController

# Create Admin Dashboard Blueprint
admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

# Dashboard View
@admin_dashboard_bp.route('/dashboard')
def dashboard():
    users = viewUserAccController.get_all_users()
    return render_template('admin/dashboard.html', users=users)

# Delete User
@admin_dashboard_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if viewUserAccController.delete_user(user_id):
        flash('User deleted successfully.', 'success')
    else:
        flash('User could not be deleted.', 'danger')
    return redirect(url_for('admin_dashboard.dashboard'))

# Edit User
@admin_dashboard_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = viewUserAccController.get_user_by_id(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role')
        isActive = bool(request.form.get('isActive'))

        success = viewUserAccController.update_user(user_id, email, phone, role, isActive)

        if success:
            flash("User updated successfully!", "success")
        else:
            flash("Failed to update user.", "danger")

        return redirect(url_for('admin_dashboard.dashboard'))

    return render_template('admin/edit_user.html', user=user)