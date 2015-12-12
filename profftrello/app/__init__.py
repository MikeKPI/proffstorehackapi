from flask import Flask
from settings import api_key, api_secret
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = "super_secret_key"

oauth = OAuth(app)

trelloapp = oauth.remote_app(
    'trello',
    consumer_key=api_key,
    consumer_secret=api_secret,
    base_url='https://api.trello.com/1/',
    request_token_url='https://trello.com/1/OAuthGetRequestToken',
    access_token_url='https://trello.com/1/OAuthGetAccessToken',
    authorize_url='https://trello.com/1/OAuthAuthorizeToken',
)

