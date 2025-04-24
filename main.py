from flask import Flask, redirect, url_for
from db_config import db, configure_db
from entity.UserAccount import User, UserProfile
from boundary.admin.createUserAcc import create_user_bp
from boundary.admin.viewUserAcc import admin_dashboard_bp 
from boundary.admin.userAdminLogin import admin_login_bp 

# Create Flask application
app = Flask(__name__)

# Configure the database
db = configure_db(app)

# Register blueprints
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(create_user_bp)
app.register_blueprint(admin_login_bp)

# Secret key for sessions and flash messages
app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production

@app.route('/')
def index():
    # Redirect to admin dashboard for now
    # In a real app, this would go to a login page
    return redirect(url_for('admin_dashboard.dashboard'))

@app.route('/admin')
def admin_index():
    return redirect(url_for('admin_dashboard.dashboard'))

@app.route('/login')
def login():
   return redirect(url_for('admin_login.login'))

if __name__ == '__main__':
    app.run(debug=True)