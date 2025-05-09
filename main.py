from flask import Flask, redirect, url_for, render_template
from db_config import db, configure_db
from entity.UserProfile import UserProfile
from entity.UserAccount import User

from boundary.admin.userAccManagementPage import user_management_bp 
from boundary.admin.userAdminLogin import admin_login_bp 
from boundary.admin.userAdminLogout import admin_logout_bp 
from boundary.admin.UserProfileManagementPage import profile_management_bp

from boundary.platformManager.CategoryManagementBoundary import CategoryManagementUI_bp
from boundary.platformManager.platformManagerLogin import platformManager_login_bp 
from boundary.platformManager.ReportManagementBoundary import reportManagementUI_bp 
from boundary.platformManager.platformManagerLogout import platformManager_logout_bp

from boundary.cleaner.cleaningServiceBoundary import CleaningServiceManagementUI_bp
from boundary.cleaner.bookingManagementBoundary import BookingManagementUI_bp
from boundary.cleaner.cleanerLogin import cleaner_login_bp 
from boundary.cleaner.cleanerLogout import cleaner_logout_bp

from boundary.homeowner.viewCleanerServicePage import CleanerServiceManagementUI_bp
from boundary.homeowner.viewBookingPage import viewBookingPage_bp
from boundary.homeowner.viewShortlistPage import viewShortlistPage_bp
from boundary.homeowner.homeownerLogin import homeowner_login_bp
from boundary.homeowner.homeownerLogout import homeowner_logout_bp

# Create Flask application
app = Flask(__name__)

# Configure the database
db = configure_db(app)

# Register blueprints
app.register_blueprint(user_management_bp)
app.register_blueprint(admin_login_bp)
app.register_blueprint(admin_logout_bp)
app.register_blueprint(profile_management_bp)

app.register_blueprint(CategoryManagementUI_bp)
app.register_blueprint(reportManagementUI_bp)
app.register_blueprint(platformManager_login_bp)
app.register_blueprint(platformManager_logout_bp)

app.register_blueprint(CleaningServiceManagementUI_bp)
app.register_blueprint(BookingManagementUI_bp)
app.register_blueprint(cleaner_login_bp)
app.register_blueprint(cleaner_logout_bp)

app.register_blueprint(CleanerServiceManagementUI_bp)
app.register_blueprint(viewBookingPage_bp)
app.register_blueprint(viewShortlistPage_bp)
app.register_blueprint(homeowner_login_bp)
app.register_blueprint(homeowner_logout_bp)

# Secret key for sessions and flash messages
app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production

@app.route('/')
def index():
    return render_template('index.html')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)