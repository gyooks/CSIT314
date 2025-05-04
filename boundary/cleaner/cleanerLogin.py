from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.cleaner.cleanerLoginController import LoginController

cleaner_login_bp = Blueprint('cleaner_login', __name__, url_prefix='/cleanerLogin')


@cleaner_login_bp.route('/', methods=['GET', 'POST'])
def cleanerLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        controller = LoginController()
        success, message = controller.login(email, password)
        if success:
            flash("Login successful!", "success")
            return redirect(url_for('CleaningServiceManagementUI.manage_services'))
        else:
            flash(message,"danger")
            return render_template('cleaner/cleanerLoginPage.html')
    return render_template('cleaner/cleanerLoginPage.html')
