from flask import Flask, redirect, url_for, render_template
from db_config import db, configure_db
from entity.UserAccount import User
from entity.UserProfile import UserProfile
from boundary.admin.createNewUser import create_user_bp
from boundary.admin.userAccManagementPage import admin_dashboard_bp 
from boundary.admin.userAdminLogin import admin_login_bp 
from boundary.admin.userAdminLogout import admin_logout_bp 
from boundary.admin.searchUserAcc import search_userAcc_bp
from boundary.admin.suspendUserAcc import suspend_user_bp
from boundary.admin.viewProfile import admin_profile_bp
from boundary.admin.UserProfileManagementPage import profile_management_bp

from boundary.platformManager.CategoryManagementBoundary import CategoryManagementUI_bp
from boundary.platformManager.platformManagerLogin import platformManager_login_bp 
from boundary.platformManager.ReportManagementBoundary import reportManagementUI_bp 

# Create Flask application
app = Flask(__name__)

# Configure the database
db = configure_db(app)

# Register blueprints
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(create_user_bp)
app.register_blueprint(admin_login_bp)
app.register_blueprint(admin_logout_bp)
app.register_blueprint(search_userAcc_bp)
app.register_blueprint(suspend_user_bp)
app.register_blueprint(admin_profile_bp)
app.register_blueprint(profile_management_bp)

app.register_blueprint(CategoryManagementUI_bp)
app.register_blueprint(reportManagementUI_bp)
app.register_blueprint(platformManager_login_bp)

# Secret key for sessions and flash messages
app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)