import requests
from flask import request

BASE_SPOTIFY_URL = 'https://api.spotify.com/v1'


def spotify_api(endpoint) -> str:
    """Make a call to spotify api for endpoint"""
    access_token: str = request.cookies.get('access_token')
    return requests.get(
        BASE_SPOTIFY_URL + endpoint,
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
