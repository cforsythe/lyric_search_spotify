from flask import Blueprint
from spotical_backend.util.spotify.auth import is_authenticated
from spotical_backend.util.spotify.api import get_user_info
from spotical_backend.util.spotify.api import get_user_playlists

bp = Blueprint('api', __name__, url_prefix='/spotify/api')


@bp.route('/user', methods=['GET'])
@is_authenticated
def user():
    return get_user_info().json()

@bp.route('/playlists', methods=['GET'])
@is_authenticated
def playlists():
    return get_user_playlists().json()
