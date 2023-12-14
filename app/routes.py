from . import app
from flask import render_template, redirect, url_for, request, session, redirect
from .github import github, get_gists, create_gist, update_gist, delete_gist, star_gist, unstar_gist, get_starred_gists
import requests

@app.route('/')
def index():
    # Retrieve user_info from session
    user_info = session.get('user_info')
    
    if user_info:
        # Process user_info
        username = user_info.get('login', 'Unknown')  # Use 'Unknown' as default if 'login' is not present

        # Check if 'access_token' is present in user_info
        access_token = user_info.get('access_token')

        if access_token:
            # Retrieve gists and starred gists using the appropriate functions
            gists = get_gists(access_token=access_token)
            starred_gists = get_starred_gists(access_token)

            # Check if gists is None
            if gists is None:
                # Handle the case when gists is None (e.g., log an error, set a default value, etc.)
                gists = []

            # Pass the 'user_info' directly to the template
            return render_template('index.html', user_info=user_info, gists=gists, starred_gists=starred_gists)

    # If user_info or access_token is not available, show the login link
    return render_template('index.html')



@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))

# Define a route for handling the GitHub OAuth authorization callback
@app.route('/login/authorized')
def authorized():
    # Get the authorization response from GitHub
    resp = github.authorized_response()

    # Check if the response or access_token is missing
    if resp is None or resp.get('access_token') is None:
        # Check if 'error_reason' key exists in request.args
        error_reason = request.args.get('error_reason', 'Unknown Reason')
        return f'Access denied: reason={error_reason} error={request.args.get("error_description", "Unknown Description")}'

    # Use the access_token to fetch user details
    user_info = github.get('user', token=(resp['access_token'], ''))

    # Check if 'login' is present in user_info
    if 'login' not in user_info.data:
        return 'Access denied: Unable to fetch user details'

    # Add the user_info to the session
    session['user_info'] = {
        'access_token': resp['access_token'],
        'login': user_info.data['login'],  # Use the correct key for login
        'scope': resp['scope'],
        'token_type': resp['token_type']
    }

    # Redirect to the home page
    return redirect(url_for('index'))

@app.route('/snippet/<gist_id>')
def snippet_detail(gist_id):
    # Retrieve user_info from session
    user_info = session.get('user_info')

    if user_info:
        # Print user_info for debugging
        print(user_info)

        # Process user_info
        username = user_info.get('login', 'Unknown')  # Use 'Unknown' as default if 'login' is not present

        # Retrieve the detailed information about the specific Gist
        gist = get_gists(gist_id=gist_id, access_token=user_info['access_token'])

        return render_template('snippet_detail.html', user_info=username, gist=gist)

    # If user_info is not available, show the login link
    return render_template('index.html')

@app.route('/snippet/create', methods=['GET', 'POST'])
def create_snippet():
    if request.method == 'POST':
        # Form submission, create a new snippet
        description = request.form.get('description')
        filename = request.form.get('filename')
        code = request.form.get('code')

        # Create the new snippet
        create_gist(description, filename, code)

        # Redirect to the index page after creating the snippet
        return redirect(url_for('index'))

    # Display the form for creating a new snippet
    return render_template('create_snippet.html')


@app.route('/snippet/edit/<gist_id>', methods=['GET', 'POST'])
def edit_snippet(gist_id):
    snippet = get_gists(gist_id)

    if request.method == 'POST':
        # Form submission, update the existing snippet
        description = request.form.get('description')
        filename = request.form.get('filename')
        code = request.form.get('code')

        # Use the provided filename if available, otherwise use the original filename
        update_gist(gist_id, description, filename, code)

        return redirect(url_for('index'))

    # Display the form for editing the snippet
    return render_template('edit_snippet.html', snippet=snippet)

@app.route('/snippet/delete/<gist_id>')
def delete_snippet(gist_id):
    delete_gist(gist_id)
    return redirect(url_for('index'))

@app.route('/snippet/star/<gist_id>')
def star_snippet(gist_id):
    star_gist(gist_id)
    return redirect(url_for('index'))

@app.route('/snippet/unstar/<gist_id>')
def unstar_snippet(gist_id):
    unstar_gist(gist_id)
    return redirect(url_for('index'))
