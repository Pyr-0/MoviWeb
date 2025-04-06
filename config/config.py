import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the absolute path to the instance folder
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_path = os.path.join(basedir, 'instance')

# Create instance directory if it doesn't exist
os.makedirs(instance_path, exist_ok=True)

class Config:
	"""Base configuration class."""
	SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(instance_path, "movie_web_app.db")}')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	OMDB_API_KEY = os.getenv('OMDB_API_KEY')
	OMDB_API_URL = 'http://www.omdbapi.com/'

class DevelopmentConfig(Config):
	"""Development configuration."""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "movie_web_app.db")}'

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