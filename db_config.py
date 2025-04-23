import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure_db(app):
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qieqie3915@localhost/cms'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the app with the extension
    db.init_app(app)
    
    return db