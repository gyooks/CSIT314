from flask import Blueprint, redirect, url_for, flash
from controller.admin.userAdminLogoutController import LogoutController

admin_logout_bp = Blueprint('admin_logout', __name__, url_prefix='/logout')


@admin_logout_bp.route('/')
def userAdminLogout():
    controller = LogoutController()
    controller.logout()
    flash("You have been logged out.", "success")
    return redirect(url_for('admin_login.userAdminLogin'))
