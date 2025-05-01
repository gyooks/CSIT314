from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.platformManager.managerLoginController import LoginController

platformManager_login_bp = Blueprint('platformManager_login', __name__, url_prefix='/PMlogin')


@platformManager_login_bp.route('/', methods=['GET', 'POST'])
def platformManagerLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        controller = LoginController()
        success, message = controller.login(email, password)
        if success:
            flash("Login successful!", "success")
            return redirect(url_for('CategoryManagementUI.manage_categories'))
            
        else:
            flash(message,"danger")
            return render_template('platformManager/platformManagerLogin.html')
    return render_template('platformManager/platformManagerLogin.html')
