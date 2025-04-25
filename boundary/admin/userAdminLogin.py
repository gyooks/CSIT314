from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.admin.userAdminLoginController import LoginController

admin_login_bp = Blueprint('admin_login', __name__, url_prefix='/login')


@admin_login_bp.route('/', methods=['GET', 'POST'])
def userAdminLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        controller = LoginController()
        success, message = controller.login(email, password)
        if success:
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard.dashboard'))
        else:
            flash(message,"danger")
            return render_template('admin/userAdminLogin.html')
    return render_template('admin/userAdminLogin.html')