import requests
from flask import current_app
from typing import Dict, Optional

class OMDbService:
	"""Service for interacting with the OMDb API."""
		
	@staticmethod
	def search_movie(title: str) -> Optional[Dict]:
		"""
		Search for a movie by title using the OMDb API.
		
		Args:
			title: The movie title to search for
			
		Returns:
			Dict containing movie information or None if not found
		"""
		try:
			params = {
				'apikey': current_app.config['OMDB_API_KEY'],
				't': title,
				'type': 'movie'
			}
			
			response = requests.get(
				current_app.config['OMDB_API_URL'],
				params=params
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get('Response') == 'True':
					return {
						'title': data.get('Title'),
						'director': data.get('Director'),
						'year': int(data.get('Year', 0)),
						'rating': float(data.get('imdbRating', 0))
					}
			return None
		except Exception as e:
			current_app.logger.error(f"Error fetching movie data from OMDb: {str(e)}")
			return None 