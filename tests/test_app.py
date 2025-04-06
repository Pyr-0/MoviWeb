import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.models import User, Movie

@pytest.fixture
def app():
	app = create_app('testing')
	with app.app_context():
		db.create_all()
		yield app
		db.session.remove()
		db.drop_all()

@pytest.fixture
def client(app):
	return app.test_client()

def test_home_page(client):
	response = client.get('/')
	assert response.status_code == 200
	assert b'Welcome' in response.data

def test_add_user(client):
	response = client.post('/add_user', data={'name': 'Test User'})
	assert response.status_code == 302  # Redirect after successful creation
	assert User.query.filter_by(name='Test User').first() is not None

def test_add_movie(client):
	# First create a user
	user = User()
	user.name = 'Test User'
	db.session.add(user)
	db.session.commit()

	# Then add a movie
	response = client.post(f'/users/{user.id}/movies/add', data={
		'title': 'Test Movie',
		'director': 'Test Director',
		'year': '2020',
		'rating': '8.5'
	})
	assert response.status_code == 302
	assert Movie.query.filter_by(title='Test Movie').first() is not None

def test_update_movie(client):
	# Create user and commit first
	user = User()
	user.name = 'Test User'
	db.session.add(user)
	db.session.commit()

	# Create movie with the committed user's ID
	movie = Movie()
	movie.title = 'Test Movie'
	movie.director = 'Test Director'
	movie.year = 2020
	movie.rating = 8.5
	movie.user_id = user.id
	db.session.add(movie)
	db.session.commit()

	# Update movie
	response = client.post(f'/users/{user.id}/movies/{movie.id}/update', data={
		'title': 'Updated Movie',
		'director': 'Updated Director',
		'year': '2021',
		'rating': '9.0'
	})
	assert response.status_code == 302
	updated_movie = Movie.query.get(movie.id)
	assert updated_movie is not None
	assert updated_movie.title == 'Updated Movie'

def test_delete_movie(client):
	# Create user and commit first
	user = User()
	user.name = 'Test User'
	db.session.add(user)
	db.session.commit()

	# Create movie with the committed user's ID
	movie = Movie()
	movie.title = 'Test Movie'
	movie.director = 'Test Director'
	movie.year = 2020
	movie.rating = 8.5
	movie.user_id = user.id
	db.session.add(movie)
	db.session.commit()

	# Delete movie
	response = client.get(f'/users/{user.id}/movies/{movie.id}/delete')
	assert response.status_code == 302
	assert Movie.query.get(movie.id) is None

def test_error_handling(client):
	# Test 404 error
	response = client.get('/nonexistent-page')
	assert response.status_code == 404
	assert b'Not Found' in response.data  # Changed to match Flask's default 404 page

	# Test 500 error (simulated)
	response = client.get('/simulate-error')
	assert response.status_code == 500
	assert b'Internal Server Error' in response.data 