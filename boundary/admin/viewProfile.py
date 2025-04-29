from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.admin.profileController import AdminProfileController

admin_profile_bp = Blueprint('admin_profile', __name__)

@admin_profile_bp.route('/admin/my-profile', methods=['GET'])
def view_my_profile():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login.login_page'))
    
    user_id = session['user_id']
    controller = AdminProfileController()
    profile_data = controller.get_admin_profile(user_id)
    
    return render_template('admin/adminProfile.html', 
                          profile_data=profile_data)

# @admin_profile_bp.route('/admin/my-profile/edit', methods=['POST'])
# def update_my_profile():
#     # Check if user is logged in
#     if 'user_id' not in session:
#         flash('Please login first', 'error')
#         return redirect(url_for('login.login_page'))
    
#     user_id = session['user_id']
#     controller = AdminProfileController()
    
#     # Get form data
#     first_name = request.form.get('first_name')
#     last_name = request.form.get('last_name')
#     phone = request.form.get('phone')
#     address = request.form.get('address')
    
#     # Update profile
#     result = controller.update_admin_profile(user_id, first_name, last_name, phone, address)
    
#     if result:
#         flash('Profile updated successfully', 'success')
#     else:
#         flash('Failed to update profile', 'error')
    
#     return redirect(url_for('admin_profile.view_my_profile'))