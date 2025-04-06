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
		config_name (str): The configuration to use ('default', 'development', 'testing', 'production')
	
	Returns:
		Flask: The configured Flask application
	"""
	# Create Flask application
	app = Flask(__name__)
	
	# Load configuration
	app.config.from_object(config[config_name])
	
	# Ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	# Initialize extensions
	db.init_app(app)
	
	# Initialize data manager
	from app.controllers.sqlite_data_manager import SQLiteDataManager
	data_manager = SQLiteDataManager()
	app.config['data_manager'] = data_manager
	
	# Register blueprints
	from app.views.routes import main_bp
	app.register_blueprint(main_bp)
	
	# Create database tables
	with app.app_context():
		db.create_all()
		print("Database tables created successfully!")
	
	return app
