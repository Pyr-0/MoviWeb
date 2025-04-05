import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from config.config import config

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(config_name='default'):
	"""
	Create and configure the Flask application.
	Args:
		config_name (str): The configuration to use
	Returns:
		Flask: The configured Flask application
	"""
	app = Flask(__name__)
		
	# Load configuration
	app.config.from_object(config[config_name])
		
	# Initialize extensions
	db.init_app(app)
		
	# Create database tables
	with app.app_context():
		db.create_all()
		
	# Register blueprints (to be added later)
	# from app.views import main_bp
	# app.register_blueprint(main_bp)
		
	return app
