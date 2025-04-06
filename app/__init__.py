from flask import Flask
from app.extensions import db
from app.controllers.sqlite_data_manager import SQLiteDataManager
from app.views.routes import main_bp
from config.config import config

def create_app(config_name='default'):
	"""Create and configure the Flask application"""
	app = Flask(__name__)
	
	# Configure the app
	app.config.from_object(config[config_name])
	
	# Initialize SQLAlchemy with the app
	db.init_app(app)
	
	# Create database tables
	with app.app_context():
		db.create_all()
	
	# Initialize the data manager
	data_manager = SQLiteDataManager()
	app.config['data_manager'] = data_manager
	
	# Register blueprints
	app.register_blueprint(main_bp)
	
	return app
