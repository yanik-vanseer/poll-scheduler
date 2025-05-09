import os
from flask import Flask
from app.db.database import db
from app.routes.poll_routes import poll_bp
from dotenv import load_dotenv

load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Function to create and configure the Flask application
def create_app():
    app = Flask(__name__)
    # Configure the MySQL database connection using environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@mysql:3306/{MYSQL_DATABASE}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the application
    db.init_app(app)

    # Create all database tables if they do not exist yet
    with app.app_context():
        db.create_all()

    # Register the blueprint for the poll related routes
    app.register_blueprint(poll_bp, url_prefix='/polls')
    return app