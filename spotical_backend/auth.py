import functools

from flask import Blueprint
from spotical_backend.util.spotify import get_client_id
from spotical_backend.util.spotify import get_client_secret
from spotical_backend.util.spotify import get_authorize_redirect
from spotical_backend.util.spotify import can_be_authenticated
from spotical_backend.util.spotify import authenticate
from flask import redirect
from requests import Response

bp = Blueprint('auth', __name__, url_prefix='/auth')

SPOTIFY_CLIENT_ID = get_client_id()
SPOTIFY_CLIENT_SECRET = get_client_secret()

@bp.route('/login', methods=['GET'])
def login():
    if can_be_authenticated():
        return authenticate()
    return get_authorize_redirect()

