import os
from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

def configure_db(app):
    # Load DB credentials from environment variables
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost") #Replace "localhost" with your db host name
    db_name = os.getenv("DB_NAME", "cms") 

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:xyyong003@localhost/cms' #replace with your: username:password@hostname/cms
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    return db 

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"), #Replace "root" with your root username
        password=os.getenv("DB_PASSWORD", "xyyong003"), #Replace "root" with your root password
        database=os.getenv("DB_NAME", "cms")
    )
