import os
import requests
from urllib.parse import urlencode
from functools import wraps
from flask import request
from flask import redirect
from flask import make_response
from spotical_backend.util.uri_manager import build_full_uri
from requests.auth import HTTPBasicAuth
from functools import lru_cache


AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'
AUTHENTICATION_URL = 'https://accounts.spotify.com/api/token'
SEVEN_DAYS_IN_SECONDS = 60*60*24*7  # seconds, minutes, hours, days
SCOPES_NEEDED = [
    'user-read-email',
    'user-read-private',
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-library-read'
]


@lru_cache(maxsize=1)
def get_client_id() -> str:
    """Retrieve spotify client_id from environment variable"""
    return os.environ.get('SPOTIFY_CLIENT_ID')


@lru_cache(maxsize=1)
def get_client_secret() -> str:
    """Retrieve spotify client_secret from environment variable"""
    return os.environ.get('SPOTIFY_CLIENT_SECRET')


def is_authenticated(func):
    """Wrapper function to verify a user has authenticated the app with spotify"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        access_token: str = request.cookies.get('access_token')
        if access_token:
            return func(*args, **kwargs)
        else:
            return redirect(build_full_uri('/login', request.args))
    return decorated_view


def can_be_authenticated() -> bool:
    """Returns True if a user has authenticated with spotify already"""
    if any([
        request.cookies.get('refresh_token'),
        request.args.get('code')
    ]):
        return True
    return False


def _get_authentication_tokens(code):
    """Get authentication to allow this app to call user specific endpoints"""
    return requests.post(
        AUTHENTICATION_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': build_full_uri('/login')
        },
        auth=HTTPBasicAuth(get_client_id(), get_client_secret())
    )


def _get_new_access_token(refresh_token):
    """If a user has already been authenticated their refresh token can be used to grab a new
    access token
    """
    return requests.post(
        AUTHENTICATION_URL,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        },
        auth=HTTPBasicAuth(get_client_id(), get_client_secret())
    )


# TODO: Add encryption for tokens
# https://medium.com/@sadnub/simple-and-secure-api-authentication-for-spas-e46bcea592ad
def authenticate():
    """Store access_token and refresh_token in user cookies"""
    refresh_token: str = request.cookies.get('refresh_token')
    auth_code: str = request.args.get('code')
    if refresh_token:
        auth_response = _get_new_access_token(refresh_token)
    elif auth_code:
        auth_response = _get_authentication_tokens(auth_code)

    auth_response_dict = auth_response.json()
    resp = make_response(redirect(build_full_uri('/', request.args)))
    resp.set_cookie(
        'access_token',
        auth_response_dict['access_token'],
        max_age=auth_response_dict['expires_in']
    )
    resp.set_cookie(
        'refresh_token',
        refresh_token or auth_response_dict['refresh_token'],
        max_age=SEVEN_DAYS_IN_SECONDS
    )
    return resp


def logout_user():
    """Remove access_token and refresh_token cookies which will 'unauthenticate' a user"""
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', '', max_age=0)
    resp.set_cookie('refresh_token', '', max_age=0)
    return resp


def get_authorize_redirect():
    """Returns a redirect for user to enable this app to call user specific spotify endpoints"""
    query_params = {
        'client_id': get_client_id(),
        'response_type': 'code',
        'redirect_uri': build_full_uri('/login', request.args),
        'scope': ' '.join(SCOPES_NEEDED)
    }
    urlencoded_params = urlencode(query_params)
    return redirect(AUTHORIZATION_URL + urlencoded_params)
