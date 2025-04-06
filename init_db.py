from app import create_app
from app.extensions import db
from app.models.models import User, Movie

def init_db():
	app = create_app()
	with app.app_context():
		# Create all tables
		db.create_all()
		
		# Add a test user if none exists
		if not User.query.first():
			test_user = User()
			test_user.name = "Test User"
			db.session.add(test_user)
			db.session.commit()
			
			# Add a test movie
			test_movie = Movie()
			test_movie.title = "The Shawshank Redemption"
			test_movie.director = "Frank Darabont"
			test_movie.year = 1994
			test_movie.rating = 9.3
			test_movie.poster_url = "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg"
			test_movie.user_id = test_user.id
			db.session.add(test_movie)
			db.session.commit()
			
		print("Database initialized successfully!")

if __name__ == '__main__':
	init_db() 