from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from app.controllers.sqlite_data_manager import SQLiteDataManager
from app.services.omdb_service import OMDbService

# Create a Blueprint for our routes
main_bp = Blueprint('main', __name__)
data_manager = SQLiteDataManager()

@main_bp.route('/')
def home():
	"""Home page route"""
	return render_template('home.html')

@main_bp.route('/users')
def list_users():
	"""List all users"""
	users = data_manager.get_all_users()
	return render_template('users.html', users=users)

@main_bp.route('/users/<int:user_id>/movies')
def user_movies(user_id):
	"""Display movies for a specific user"""
	movies = data_manager.get_user_movies(user_id)
	return render_template('user_movies.html', movies=movies, user_id=user_id)

@main_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
	"""Add a new user"""
	if request.method == 'POST':
		name = request.form.get('name')
		if not name:
			flash('Name is required!', 'error')
			return redirect(url_for('main.add_user'))
		
		user = data_manager.add_user(name)
		
		if user:
			flash('User added successfully!', 'success')
			return redirect(url_for('main.list_users'))
		else:
			flash('Error adding user!', 'error')
			return redirect(url_for('main.add_user'))
		
	return render_template('add_user.html')

@main_bp.route('/users/<int:user_id>/movies/add', methods=['GET', 'POST'])
def add_movie(user_id):
	"""Add a new movie for a user"""
	if request.method == 'POST':
		title = request.form.get('title')
		if not title:
			flash('Title is required', 'error')
			return redirect(url_for('main.add_movie', user_id=user_id))
		
		# Try to fetch movie data from OMDb
		movie_data = OMDbService.search_movie(title)
		
		if movie_data:
			# Use data from OMDb
			movie = data_manager.add_movie(
				user_id=user_id,
				title=movie_data['title'],
				director=movie_data['director'],
				year=movie_data['year'],
				rating=movie_data['rating']
			)
			if movie:
				flash('Movie added successfully using OMDb data!', 'success')
			else:
				flash('Error adding movie', 'error')
		else:
			# Fall back to manual input
			director = request.form.get('director', '')
			year = request.form.get('year')
			rating = request.form.get('rating')
			
			# Validate year and rating
			try:
				year = int(year) if year else 0
				rating = float(rating) if rating else 0.0
				
				if year < 1888 or year > datetime.now().year:
					flash('Invalid year. Must be between 1888 and current year.', 'error')
					return redirect(url_for('main.add_movie', user_id=user_id))
				
				if rating < 0 or rating > 10:
					flash('Invalid rating. Must be between 0 and 10.', 'error')
					return redirect(url_for('main.add_movie', user_id=user_id))
				
				movie = data_manager.add_movie(
					user_id=user_id,
					title=title,
					director=director,
					year=year,
					rating=rating
				)
				if movie:
					flash('Movie added successfully!', 'success')
				else:
					flash('Error adding movie', 'error')
			except ValueError:
				flash('Invalid input for year or rating', 'error')
				return redirect(url_for('main.add_movie', user_id=user_id))
		
		return redirect(url_for('main.user_movies', user_id=user_id))
	
	return render_template('add_movie.html', 
						 user_id=user_id,
						 current_year=datetime.now().year)

@main_bp.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
	"""Update a movie"""
	movie = data_manager.get_movie(movie_id)
	if not movie:
		flash('Movie not found', 'error')
		return redirect(url_for('main.user_movies', user_id=user_id))
	
	if request.method == 'POST':
		title = request.form.get('title')
		if not title:
			flash('Title is required', 'error')
			return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
		
		director = request.form.get('director', '')
		year = int(request.form.get('year', 0))
		rating = float(request.form.get('rating', 0))
		
		updated_movie = data_manager.update_movie(
			movie_id=movie_id,
			title=title,
			director=director,
			year=year,
			rating=rating
		)
		if updated_movie:
			flash('Movie updated successfully!', 'success')
		else:
			flash('Error updating movie', 'error')
		return redirect(url_for('main.user_movies', user_id=user_id))
	
	return render_template('update_movie.html', movie=movie, user_id=user_id)

@main_bp.route('/users/<int:user_id>/movies/<int:movie_id>/delete')
def delete_movie(user_id, movie_id):
	"""Delete a movie"""
	if data_manager.delete_movie(movie_id):
		flash('Movie deleted successfully!', 'success')
	else:
		flash('Error deleting movie', 'error')
	return redirect(url_for('main.user_movies', user_id=user_id)) 