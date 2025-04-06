from datetime import datetime
from app.extensions import db


class User(db.Model):
	"""
	User model representing a user in the system.
	"""
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	movies = db.relationship('Movie', backref='user', lazy=True, cascade='all, delete-orphan')

	def to_dict(self):
		"""
		Convert user object to dictionary.
		Returns:
			dict: User data
		"""
		return {
			'id': self.id,
			'name': self.name,
			'created_at': self.created_at.isoformat(),
			'movie_count': len(self.movies)
		}


class Movie(db.Model):
	"""
	Movie model representing a movie in a user's collection.
	"""
	__tablename__ = 'movies'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	director = db.Column(db.String(100))
	year = db.Column(db.Integer)
	rating = db.Column(db.Float)
	poster_url = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	def to_dict(self):
		"""
		Convert movie object to dictionary.
		Returns:
			dict: Movie data
		"""
		return {
			'id': self.id,
			'title': self.title,
			'director': self.director,
			'year': self.year,
			'rating': self.rating,
			'poster_url': self.poster_url,
			'user_id': self.user_id,
			'created_at': self.created_at.isoformat()
		} 