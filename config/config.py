import os

# Get the absolute path to the instance folder
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_path = os.path.join(basedir, 'instance')

# Create instance directory if it doesn't exist
os.makedirs(instance_path, exist_ok=True)

class Config:
	"""Base configuration"""
	# Generate a random secret key
	SECRET_KEY = os.urandom(24)
	
	# Database configuration
	DATABASE_PATH = os.path.join(instance_path, 'moviwebapp.db')
	
	# Debug mode
	DEBUG = True
	
	# OMDb API configuration
	OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'your_api_key_here')  # Replace with your actual API key
	OMDB_API_URL = 'http://www.omdbapi.com/'

class DevelopmentConfig(Config):
	"""Development configuration."""
	SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "moviwebapp.db")}'

class TestingConfig(Config):
	"""Testing configuration."""
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
	"""Production configuration."""
	DEBUG = False

# Configuration dictionary
config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
} 