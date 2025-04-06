from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from datetime import datetime
from app.controllers.sqlite_data_manager import SQLiteDataManager
from app.services.omdb_service import OMDbService

# Create a Blueprint for our routes
main_bp = Blueprint('main', __name__)
data_manager = SQLiteDataManager()

def register_error_handlers(app):
	"""Register error handlers at the application level"""
	@app.errorhandler(404)
	def page_not_found(e):
		"""Handle 404 Not Found errors"""
		return render_template('404.html'), 404

	@app.errorhandler(500)
	def internal_server_error(e):
		"""Handle 500 Internal Server Error"""
		return render_template('500.html'), 500
		
	@app.errorhandler(403)
	def forbidden(e):
		"""Handle 403 Forbidden errors"""
		return render_template('403.html'), 403
		
	@app.errorhandler(405)
	def method_not_allowed(e):
		"""Handle 405 Method Not Allowed errors"""
		return render_template('405.html'), 405

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
	try:
		user = data_manager.get_user(user_id)
		if not user:
			flash('User not found!', 'error')
			abort(404)
			
		movies = data_manager.get_user_movies(user_id)
		if not movies:
			flash('No movies found for this user. Add some movies to get started!', 'info')
			
		return render_template('user_movies.html', user=user, movies=movies)
	except Exception as e:
		flash('An error occurred while loading the user\'s movies.', 'error')
		current_app.logger.error(f"Error in user_movies route: {str(e)}")
		return redirect(url_for('main.list_users'))

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
	"""Add a new movie for a user
	
	This route handles both displaying the add movie form and processing the form submission.
	When a movie title is submitted, it first attempts to fetch data from OMDb.
	If OMDb data is not available, it uses the manually entered data.
	
	Args:
		user_id: The ID of the user adding the movie
		
	Returns:
		On GET: Renders the add movie form
		On POST: Redirects to the user's movies page with a success/error message
	"""
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
				rating=movie_data['rating'],
				poster_url=movie_data['poster_url']
			)
			if movie:
				flash('Movie added successfully using OMDb data!', 'success')
			else:
				flash('Error adding movie', 'error')
		else:
			# Use manually entered data
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
					rating=rating,
					poster_url=''  # No poster URL for manually added movies
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
	try:
		if request.method == 'POST':
			title = request.form.get('title')
			director = request.form.get('director', '')
			year = request.form.get('year')
			rating = request.form.get('rating')
			
			if not title:
				flash('Title is required', 'error')
				return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
			
			try:
				year = int(year) if year else 0
				rating = float(rating) if rating else 0.0
				
				if year < 1888 or year > datetime.now().year:
					flash('Invalid year. Must be between 1888 and current year.', 'error')
					return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
				
				if rating < 0 or rating > 10:
					flash('Invalid rating. Must be between 0 and 10.', 'error')
					return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
				
				# Try to fetch new data from OMDb if title changed
				movie = data_manager.get_movie(movie_id)
				if not movie:
					flash('Movie not found', 'error')
					return redirect(url_for('main.user_movies', user_id=user_id))
					
				if movie.title != title:
					movie_data = OMDbService.search_movie(title)
					if movie_data:
						director = movie_data['director']
						year = movie_data['year']
						rating = movie_data['rating']
						poster_url = movie_data['poster_url']
					else:
						poster_url = movie.poster_url  # Keep existing poster if OMDb lookup fails
				else:
					poster_url = movie.poster_url  # Keep existing poster if title didn't change
				
				movie = data_manager.update_movie(
					movie_id=movie_id,
					title=title,
					director=director,
					year=year,
					rating=rating,
					poster_url=poster_url
				)
				
				if movie:
					flash('Movie updated successfully!', 'success')
					return redirect(url_for('main.user_movies', user_id=user_id))
				else:
					flash('Error updating movie', 'error')
					return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
					
			except ValueError:
				flash('Invalid input for year or rating', 'error')
				return redirect(url_for('main.update_movie', user_id=user_id, movie_id=movie_id))
		
		movie = data_manager.get_movie(movie_id)
		if not movie:
			abort(404)
			
		return render_template('update_movie.html', 
							 movie=movie,
							 user_id=user_id,
							 current_year=datetime.now().year)
							 
	except Exception as e:
		flash('An error occurred while updating the movie', 'error')
		return redirect(url_for('main.user_movies', user_id=user_id))

@main_bp.route('/users/<int:user_id>/movies/<int:movie_id>/delete')
def delete_movie(user_id, movie_id):
	"""Delete a movie"""
	try:
		success = data_manager.delete_movie(movie_id)
		if success:
			flash('Movie deleted successfully!', 'success')
		else:
			flash('Error deleting movie', 'error')
	except Exception as e:
		flash('An error occurred while deleting the movie', 'error')
	
	return redirect(url_for('main.user_movies', user_id=user_id))

@main_bp.route('/simulate-error')
def simulate_error():
	"""Route to simulate a 500 error for testing"""
	abort(500) 