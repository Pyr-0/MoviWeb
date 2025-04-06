from typing import List, Dict, Optional
from flask import current_app
from app.controllers.data_manager_interface import DataManagerInterface
from app.models.models import User, Movie
from app.extensions import db

class SQLiteDataManager(DataManagerInterface):
	"""SQLite implementation of the DataManagerInterface using SQLAlchemy."""
	
	def __init__(self):
		"""Initialize the SQLite data manager."""
		self.db = db
	
	def get_all_users(self) -> List[User]:
		"""Retrieve all users from the database."""
		return User.query.all()
	
	def get_user_movies(self, user_id: int) -> List[Movie]:
		"""Retrieve all movies for a specific user."""
		return Movie.query.filter_by(user_id=user_id).all()
	
	def get_movie(self, movie_id: int) -> Optional[Movie]:
		"""Retrieve a movie from the database."""
		return Movie.query.get(movie_id)
	
	def add_user(self, name: str) -> Optional[User]:
		"""Add a new user to the database."""
		if not name:
			return None
		
		try:
			user = User(name=name)
			self.db.session.add(user)
			self.db.session.commit()
			return user
		except Exception:
			self.db.session.rollback()
			return None
	
	def add_movie(self, user_id: int, title: str, director: str, year: int, rating: float) -> Optional[Movie]:
		"""Add a new movie to a user's collection."""
		if not title:
			return None
		
		try:
			movie = Movie(
				user_id=user_id,
				title=title,
				director=director,
				year=year,
				rating=rating
			)
			self.db.session.add(movie)
			self.db.session.commit()
			return movie
		except Exception:
			self.db.session.rollback()
			return None
	
	def update_movie(self, movie_id: int, title: str, director: str, year: int, rating: float) -> Optional[Movie]:
		"""Update an existing movie in a user's collection."""
		try:
			movie = Movie.query.get(movie_id)
			if not movie:
				return None
			
			movie.title = title
			movie.director = director
			movie.year = year
			movie.rating = rating
			
			self.db.session.commit()
			return movie
		except Exception:
			self.db.session.rollback()
			return None
	
	def delete_movie(self, movie_id: int) -> bool:
		"""Delete a movie from a user's collection."""
		try:
			movie = Movie.query.get(movie_id)
			if not movie:
				return False
			
			self.db.session.delete(movie)
			self.db.session.commit()
			return True
		except Exception:
			self.db.session.rollback()
			return False 