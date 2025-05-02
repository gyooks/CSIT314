# Run this in terminal "python HashingPassword.py",  it will hash the current password in database

from werkzeug.security import generate_password_hash
from entity.UserAccount import User
from db_config import db
from main import app  # Import the app instance from main.py

def migrate_passwords():
    users = User.query.all()

    for user in users:
        if user.password and not user.password.startswith('pbkdf2:'):
            print(f"Hashing password for user: {user.email}")
            user.password = generate_password_hash(user.password)

    db.session.commit()
    print("Password migration complete.")

if __name__ == "__main__":
    # Ensure the application context is pushed
    with app.app_context():
        migrate_passwords()
