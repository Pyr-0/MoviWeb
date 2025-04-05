from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
	"""
	Abstract base class defining the interface for data management.
	All data manager implementations must inherit from this class
	and implement its abstract methods.
	"""

	@abstractmethod
	def get_all_users(self):
		"""
		Retrieve all users from the data source.
		Returns:
			list: A list of user dictionaries
		"""
		pass

	@abstractmethod
	def get_user_movies(self, user_id):
		"""
		Retrieve all movies for a specific user.
		Args:
			user_id (int): The ID of the user
		Returns:
			list: A list of movie dictionaries
		"""
		pass

	@abstractmethod
	def add_user(self, user_data):
		"""
		Add a new user to the data source.
		Args:
			user_data (dict): Dictionary containing user information
		Returns:
			dict: The created user data
		"""
		pass

	@abstractmethod
	def add_movie(self, user_id, movie_data):
		"""
		Add a new movie to a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_data (dict): Dictionary containing movie information
		Returns:
			dict: The created movie data
		"""
		pass

	@abstractmethod
	def update_movie(self, user_id, movie_id, movie_data):
		"""
		Update an existing movie in a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_id (int): The ID of the movie
			movie_data (dict): Dictionary containing updated movie information
		Returns:
			dict: The updated movie data
		"""
		pass

	@abstractmethod
	def delete_movie(self, user_id, movie_id):
		"""
		Delete a movie from a user's collection.
		Args:
			user_id (int): The ID of the user
			movie_id (int): The ID of the movie
		Returns:
			bool: True if deletion was successful, False otherwise
		"""
		pass 