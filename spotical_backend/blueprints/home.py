from flask import Blueprint
import json

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    return json.dumps(
        {   
            'api': 'Spotical Web API',
            'owner': 'https://github.com/cforsythe',
        }   
    ) 
