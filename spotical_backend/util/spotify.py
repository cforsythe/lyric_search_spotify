import os
import requests
from urllib.parse import urlencode
from functools import wraps
from flask import Response
from flask import request 
from flask import redirect
from flask import make_response 
import json

AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'
AUTHENTICATION_URL = 'https://accounts.spotify.com/api/token' 
SEVEN_DAYS_IN_SECONDS = 60*60*24*7 # seconds, minutes, hours, days


#TODO: Add caching
def get_client_id() -> str:
    return os.environ.get('SPOTIFY_CLIENT_ID')


#TODO: Add caching
def get_client_secret() -> str:
    return os.environ.get('SPOTIFY_CLIENT_SECRET')


def create_response_object(status_code: str):
    response = Response()
    response.status_code = status_code
    return response


def is_authenticated(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        access_token: str = request.cookies.get('access_token')
        if access_token:
            return func(*args, **kwargs)
        else:
            return redirect('http://localhost:5000/auth/login?' + urlencode(request.args))
    return decorated_view


def can_be_authenticated():
    if any([
        request.cookies.get('refresh_token'),
        request.args.get('code')
    ]):
        return True
    return False


def _get_authentication_tokens(code):
    return requests.post(
        AUTHENTICATION_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:5000/home',
            'client_id': get_client_id(),
            'client_secret': get_client_secret(),
        }
    )


#TODO: Add encryption for tokens
def authenticate():
    refresh_token: str = request.cookies.get('refresh_token')
    auth_code: str = request.args.get('code')
    if refresh_token:
        auth_response = _get_authentication_tokens(refresh_token)
    elif auth_code:
        auth_response = _get_authentication_tokens(auth_code)

    auth_response_dict = auth_response.json()
    resp = make_response(redirect('http://localhost:5000/home'))
    resp.set_cookie(
        'access_token',
        auth_response_dict['access_token'],
        max_age=auth_response_dict['expires_in']
    )
    resp.set_cookie(
        'refresh_token',
        auth_response_dict['refresh_token'],
        max_age=SEVEN_DAYS_IN_SECONDS 
    )
    return resp


def get_authorize_redirect():
    query_params={
        'client_id': get_client_id(),
        'response_type': 'code',
        'redirect_uri': 'http://localhost:5000/home',
        'scope': 'user-read-email user-read-private'
    }
    urlencoded_params = urlencode(query_params)
    return redirect(AUTHORIZATION_URL + urlencoded_params)


def get_user_info():
    access_token = request.cookies.get('access_token')
    return requests.get('https://api.spotify.com/v1/me', headers={'Authorization': f'Bearer {access_token}'})
