import requests
from flask import request

BASE_SPOTIFY_URL = 'https://api.spotify.com/v1'


def get_user_info() -> str:
    """Get info about a users spotify account"""
    access_token = request.cookies.get('access_token')
    return requests.get(BASE_SPOTIFY_URL + '/me', headers={'Authorization': f'Bearer {access_token}'})


# TODO: Add ability to use limit and offset
# https://developer.spotify.com/documentation/web-api/reference/playlists
# /get-a-list-of-current-users-playlists/
def get_user_playlists() -> str:
    """Retrieve 20 of a users playlist"""
    access_token = request.cookies.get('access_token')
    return requests.get(BASE_SPOTIFY_URL + '/me/playlists', headers={'Authorization': f'Bearer {access_token}'})

