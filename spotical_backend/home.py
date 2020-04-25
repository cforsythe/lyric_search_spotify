import functools

from flask import Blueprint
from flask import make_response
from flask import request
from spotical_backend.util.spotify import is_authenticated
from spotical_backend.util.spotify import get_user_info

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/home', methods=['GET'])
@is_authenticated
def home():
    return get_user_info().json()
