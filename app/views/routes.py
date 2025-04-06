from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.sqlite_data_manager import SQLiteDataManager

# Create a Blueprint for our routes
main_bp = Blueprint('main', __name__)

# Initialize the data manager
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

@main_bp.route('/users/<int:user_id>')
def user_movies(user_id):
    """Display movies for a specific user"""
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', movies=movies, user_id=user_id)

@main_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        user_data = {
            'name': request.form['name']
        }
        result = data_manager.add_user(user_data)
        if result:
            flash('User added successfully!', 'success')
            return redirect(url_for('main.list_users'))
        else:
            flash('Error adding user', 'error')
    return render_template('add_user.html')

@main_bp.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a new movie for a user"""
    if request.method == 'POST':
        movie_data = {
            'title': request.form['title'],
            'director': request.form.get('director'),
            'year': request.form.get('year'),
            'rating': request.form.get('rating')
        }
        result = data_manager.add_movie(user_id, movie_data)
        if result:
            flash('Movie added successfully!', 'success')
            return redirect(url_for('main.user_movies', user_id=user_id))
        else:
            flash('Error adding movie', 'error')
    return render_template('add_movie.html', user_id=user_id)

@main_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update a movie"""
    if request.method == 'POST':
        movie_data = {
            'title': request.form['title'],
            'director': request.form.get('director'),
            'year': request.form.get('year'),
            'rating': request.form.get('rating')
        }
        result = data_manager.update_movie(user_id, movie_id, movie_data)
        if result:
            flash('Movie updated successfully!', 'success')
            return redirect(url_for('main.user_movies', user_id=user_id))
        else:
            flash('Error updating movie', 'error')
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id)

@main_bp.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """Delete a movie"""
    if data_manager.delete_movie(user_id, movie_id):
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Error deleting movie', 'error')
    return redirect(url_for('main.user_movies', user_id=user_id)) 