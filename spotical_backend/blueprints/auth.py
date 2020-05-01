import functools

from flask import Blueprint
from spotical_backend.util.spotify.auth import get_authorize_redirect
from spotical_backend.util.spotify.auth import can_be_authenticated
from spotical_backend.util.spotify.auth import authenticate
from requests import Response

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/login', methods=['GET'])
def login():
    if can_be_authenticated():
        return authenticate()
    return get_authorize_redirect()

