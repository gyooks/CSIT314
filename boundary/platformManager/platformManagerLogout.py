from flask import Blueprint, redirect, url_for, flash
from controller.platformManager.platformManagerLogoutController import LogoutController

platformManager_logout_bp = Blueprint('platformManager_logout', __name__, url_prefix='/PMlogout')


@platformManager_logout_bp.route('/')
def platformManagerLogout():
    controller = LogoutController()
    controller.logout()
    flash("You have been logged out.", "success")
    return redirect(url_for('platformManager_login.platformManagerLogin'))
