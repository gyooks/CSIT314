from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.admin.createUserAccController import createUserAccController

# Create User Account Blueprint
create_user_bp = Blueprint('create_user', __name__, url_prefix='/admin')

@create_user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    
    # This would typically have authentication checks to ensure only admins can access
    if 'user_id' not in session:
        flash("You must be logged in to perform this action", "danger")
        return redirect(url_for('admin_login.userAdminLogin'))
    user_id = session['user_id']
        
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        phone = request.form.get('phone')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        
        # Basic validation
        if not email or not password or not role:
            flash('Email, password, and role are required fields', 'error')
            return render_template('admin/createUserAccPage.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('admin/createUserAccPage.html')
        
        # Create user
        success, message = createUserAccController.create_user(
            email=email,
            password=password,
            role=role,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            address=address
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('admin_dashboard.dashboard'))  # Updated to use new blueprint name
        else:
            flash(message, 'error')
            return render_template('admin/createUserAccPage.html')
    
    # GET request - show the form
    return render_template('admin/createUserAccPage.html')