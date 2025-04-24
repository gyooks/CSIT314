import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure_db(app):
    # Load DB credentials from environment variables
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "YourPassword")
    host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "cms")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://scrumlord:scrumlord@localhost/scrumlorddb' #Admin for ur db:password@localhost/db name 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    return db 