import requests
from flask import current_app
from typing import Dict, Optional

class OMDbService:
	"""Service for interacting with the OMDb API.
	
	This service provides methods to fetch movie data from the OMDb API.
	It handles API authentication, request formatting, and response parsing.
	"""
		
	@staticmethod
	def search_movie(title: str) -> Optional[Dict]:
		"""
		Search for a movie by title using the OMDb API.
		
		Args:
			title: The movie title to search for
			
		Returns:
			Dict containing movie information with the following keys:
				- title (str): Movie title
				- director (str): Movie director(s)
				- year (int): Release year
				- rating (float): IMDb rating (0-10)
				- poster_url (str): URL to the movie poster image
			Returns None if the movie is not found or if an error occurs
			
		Raises:
			No exceptions are raised. All errors are logged and None is returned.
		"""
		api_key = current_app.config['OMDB_API_KEY']
		base_url = current_app.config['OMDB_API_URL']
		
		params = {
			'apikey': api_key,
			't': title,
			'plot': 'short'
		}
		
		try:
			response = requests.get(base_url, params=params)
			response.raise_for_status()
			data = response.json()
			
			if data.get('Response') == 'True':
				return {
					'title': data.get('Title', ''),
					'director': data.get('Director', ''),
					'year': int(data.get('Year', 0)),
					'rating': float(data.get('imdbRating', 0)),
					'poster_url': data.get('Poster', '')
				}
			return None
		except (requests.RequestException, ValueError, KeyError) as e:
			current_app.logger.error(f"Error fetching movie data from OMDb: {str(e)}")
			return None 