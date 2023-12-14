from flask import Flask
from flask_oauthlib.client import OAuth

app = Flask(__name__)

app.secret_key = '931fda787adc598bac439783d29a42c33bbf7b1475070004'
oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='4763954805253af2f48c',
    consumer_secret='f90e0d25d25d3b33ec71da4c837bc303ad4b9dff',
    request_token_params={'scope': 'gist'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

from app import routes