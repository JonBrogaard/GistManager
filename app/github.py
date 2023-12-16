from flask_oauthlib.client import OAuth
from flask import current_app, session
from . import app
import requests

# Define the GitHub API base URL
GITHUB_API_URL = 'https://api.github.com'

# Initialize OAuth extension with the Flask app
oauth = OAuth(current_app)

# Configure GitHub OAuth settings
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

# Define a function to get the GitHub OAuth token from the session
@github.tokengetter
def get_github_oauth_token():
    user_info = session.get('user_info')
    if user_info:
        return user_info.get('access_token')

def get_gists(gist_id=None, access_token=None):
    if not access_token:
        # Retrieve the access token from the session if not provided
        access_token = get_github_oauth_token()
       
    if gist_id:
        # Fetch details for a specific Gist
        url = f'{GITHUB_API_URL}/gists/{gist_id}'
    else:
        # Fetch a list of Gists
        url = f'{GITHUB_API_URL}/gists'

    headers = {}
    if access_token:
        headers['Authorization'] = 'Bearer ' + access_token

    response = requests.get(url, headers=headers)
    return response.json()

# Define functions for creating, updating, and deleting Gists
def create_gist(description, filename, code):
    url = f'{GITHUB_API_URL}/gists'
    data = {
        'description': description,
        'public': False,
        'files': {filename: {'content': code}}
    }
    response = requests.post(url, json=data, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})
    return response.json()

def update_gist(gist_id, description, filename, code):
    url = f'{GITHUB_API_URL}/gists/{gist_id}'
    data = {
        'description': description,
        'files': {filename: {'content': code}}
    }
    response = requests.patch(url, json=data, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})
    return response.json()

def delete_gist(gist_id):
    url = f'{GITHUB_API_URL}/gists/{gist_id}'
    response = requests.delete(url, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})
    return response.status_code

def get_gist_comments(gist_id):
    url = f'{GITHUB_API_URL}/gists/{gist_id}/comments'
    response = requests.get(url, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})
    return response.json()

def comment_gist(gist_id, comment):
    url = f'{GITHUB_API_URL}/gists/{gist_id}/comments'
    data = {'body': comment}
    response = requests.post(url, json=data, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})

    if response.status_code == 201:
        print('Comment added successfully')
    else:
        print(f'Failed to add comment. Status Code: {response.status_code}, Response: {response.text}')

def comment_delete(gist_id, comment_id):
    url = f'{GITHUB_API_URL}/gists/{gist_id}/comments/{comment_id}'
    response = requests.delete(url, headers={'Authorization': 'Bearer ' + get_github_oauth_token()})

    if response.status_code == 204:
        print('Comment deleted successfully')
    else:
        print(f'Failed to delete comment. Status Code: {response.status_code}, Response: {response.text}')

# OAuth token retrieval function
def get_github_token():
    user_info = session.get('user_info')
    if user_info:
        return user_info.get('access_token')