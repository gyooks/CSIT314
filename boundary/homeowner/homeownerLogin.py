from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.homeowner.homeownerLoginController import LoginController

homeowner_login_bp = Blueprint('homeowner_login', __name__, url_prefix='/HomeownerLogin')


@homeowner_login_bp.route('/', methods=['GET', 'POST'])
def homeownerLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        controller = LoginController()
        success, message = controller.login(email, password)
        if success:
            flash("Login successful!", "success")
            return redirect(url_for('CleanerServiceManagementUI.view_services'))
        else:
            flash(message,"danger")
            return render_template('homeowner/homeownerLoginPage.html')
    return render_template('homeowner/homeownerLoginPage.html')
