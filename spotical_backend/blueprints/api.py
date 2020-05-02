from flask import Blueprint
from spotical_backend.util.spotify.auth import is_authenticated
from spotical_backend.util.spotify.api import spotify_api

bp = Blueprint('api', __name__, url_prefix='/spotify/api')


@bp.route('/user', methods=['GET'])
@is_authenticated
def user():
    return spotify_api('/me').json()


@bp.route('/playlists', methods=['GET'])
@is_authenticated
def playlists():
    return spotify_api('/me/playlists').json()


# TODO: Add ability to use limit and offset
# https://developer.spotify.com/documentation/web-api/reference/playlists
# /get-a-list-of-current-users-playlists/
@bp.route('/playlists/<playlist_id>', methods=['GET'])
@is_authenticated
def get_playlist_by_id(playlist_id):
    return spotify_api(f'/playlists/{playlist_id}').json()


@bp.route('/me/tracks', methods=['GET'])
@is_authenticated
def my_tracks():
    return spotify_api('/me/tracks').json()
