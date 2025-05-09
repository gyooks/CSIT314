from flask import Blueprint, redirect, url_for, flash
from controller.cleaner.cleanerLogoutController import LogoutController

cleaner_logout_bp = Blueprint('cleaner_logout', __name__, url_prefix='/cleanerlogout')


@cleaner_logout_bp.route('/')
def cleanerLogout():
    controller = LogoutController()
    controller.logout()
    flash("You have been logged out.", "success")
    return redirect(url_for('cleaner_login.cleanerLogin'))

