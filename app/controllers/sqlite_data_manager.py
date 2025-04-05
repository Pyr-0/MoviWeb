from typing import List, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import db, User, Movie
from .data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
	"""
	SQLite implementation of the DataManagerInterface.
	Handles all database operations using SQLAlchemy ORM.
	"""

	def get_all_users(self) -> List[Dict]:
		"""
		Retrieve all users from the database.
		Returns:
			List[Dict]: List of user dictionaries
		"""
		try:
			users = User.query.all()
			return [user.to_dict() for user in users]
		except SQLAlchemyError as e:
			print(f"Error getting users: {str(e)}")
			return []

	def get_user_movies(self, user_id: int) -> List[Dict]:
		"""
		Retrieve all movies for a specific user.
		Args:
			user_id (int): The ID of the user
		Returns:
			List[Dict]: List of movie dictionaries
		"""
		try:
			movies = Movie.query.filter_by(user_id=user_id).all()
			return [movie.to_dict() for movie in movies]
		except SQLAlchemyError as e:
			print(f"Error getting user movies: {str(e)}")
			return []

	def add_user(self, user_data: Dict) -> Optional[Dict]:
		"""
		Add a new user to the database.
		Args:
			user_data (Dict): Dictionary containing user information
		Returns:
			Optional[Dict]: The created user data or None if failed
		"""
		try:
			new_user = User(**user_data)
			db.session.add(new_user)
			db.session.commit()
			return new_user.to_dict()
		except SQLAlchemyError as e:
			db.session.rollback()
			print(f"Error adding user: {str(e)}")
			return None

	def add_movie(self, user_id: int, movie_data: Dict) -> Optional[Dict]:
		"""
		Add a new movie to a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_data (Dict): Dictionary containing movie information
		Returns:
			Optional[Dict]: The created movie data or None if failed
		"""
		try:
			movie_data['user_id'] = user_id
			new_movie = Movie(**movie_data)
			db.session.add(new_movie)
			db.session.commit()
			return new_movie.to_dict()
		except SQLAlchemyError as e:
			db.session.rollback()
			print(f"Error adding movie: {str(e)}")
			return None

	def update_movie(self, user_id: int, movie_id: int, movie_data: Dict) -> Optional[Dict]:
		"""
		Update an existing movie in a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_id (int): The ID of the movie
			movie_data (Dict): Dictionary containing updated movie information
		Returns:
			Optional[Dict]: The updated movie data or None if failed
		"""
		try:
			movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
			if not movie:
				return None

			for key, value in movie_data.items():
				if hasattr(movie, key):
					setattr(movie, key, value)

			db.session.commit()
			return movie.to_dict()
		except SQLAlchemyError as e:
			db.session.rollback()
			print(f"Error updating movie: {str(e)}")
			return None

	def delete_movie(self, user_id: int, movie_id: int) -> bool:
		"""
		Delete a movie from a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_id (int): The ID of the movie
		Returns:
			bool: True if deletion was successful, False otherwise
		"""
		try:
			movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
			if not movie:
				return False

			db.session.delete(movie)
			db.session.commit()
			return True
		except SQLAlchemyError as e:
			db.session.rollback()
			print(f"Error deleting movie: {str(e)}")
			return False 