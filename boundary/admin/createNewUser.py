from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.admin.createUserAccController import createUserAccController
from controller.admin.createUserProfileController import createUserProfileController

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
        
        # Step 1: Create user account
        success, message, new_user_id = createUserAccController.create_user(
            email=email,
            password=password,
            role=role
        )
        
        if not success:
            flash(message, 'error')
            return render_template('admin/createUserAccPage.html')
        
        # Step 2: Create user profile if account creation was successful
        if first_name or last_name:
            profile_success, profile_message = createUserProfileController.create_profile(
                user_id=new_user_id,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone
            )
            
            if not profile_success:
                # Profile creation failed, but account already created
                flash(f"Account created but profile creation failed: {profile_message}", 'warning')
                return redirect(url_for('admin_dashboard.dashboard'))
                
            flash("User created successfully", 'success')
        else:
            flash("User account created successfully", 'success')
            
        return redirect(url_for('admin_dashboard.dashboard'))
    
    # GET request - show the form
    return render_template('admin/createUserAccPage.html')