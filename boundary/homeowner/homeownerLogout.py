from flask import Blueprint, redirect, url_for, flash
from controller.homeowner.homeownerLogoutController import LogoutController

homeowner_logout_bp = Blueprint('homeowner_logout', __name__, url_prefix='/homeownerlogout')


@homeowner_logout_bp.route('/')
def homeownerLogout():
    controller = LogoutController()
    controller.logout()
    flash("You have been logged out.", "success")
    return redirect(url_for('homeowner_login.homeownerLogin'))