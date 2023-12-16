from . import app
from flask import render_template, redirect, url_for, request, session, redirect
from .github import github, get_gists, create_gist, update_gist, delete_gist, get_gist_comments, comment_gist, comment_delete
import requests
from datetime import datetime

def time_ago(timestamp):
    created_at = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.utcnow()
    delta = now - created_at

    if delta.seconds < 60:
        return f"{delta.seconds} seconds"
    elif delta.seconds < 3600:
        minutes = delta.seconds // 60
        return f"{minutes} minutes"
    else:
        hours = delta.seconds // 3600
        return f"{hours} hours"

@app.route('/')
def index():
    # Retrieve user_info from session
    user_info = session.get('user_info')
    
    if user_info:

        username = user_info.get('login', 'Unknown')  

        access_token = user_info.get('access_token')

        if access_token:

            gists = get_gists(access_token=access_token)

            if gists is None:
                gists = []

            # Retrieve comments for each gist
            comments = [get_gist_comments(gist['id']) for gist in gists]

            # Pass the 'user_info' directly to the template
            return render_template('index.html', user_info=username, gists=gists, comments=comments, time_ago=time_ago)

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
        'login': user_info.data['login'],  
        'scope': resp['scope'],
        'token_type': resp['token_type']
    }

    return redirect(url_for('index'))

@app.route('/snippet/<gist_id>')
def snippet_detail(gist_id):
    # Retrieve user_info from session
    user_info = session.get('user_info')

    if user_info:
        # Process user_info
        username = user_info.get('login', 'Unknown')  # Use 'Unknown' as default if 'login' is not present

        # Retrieve the detailed information about the specific Gist
        gist = get_gists(gist_id=gist_id, access_token=user_info['access_token'])

        if gist is None:
            # Redirect to the index page if the Gist is not found
            return redirect(url_for('index'))

        # Fetch comments for the gist
        comments = get_gist_comments(gist_id)

        return render_template('snippet_detail.html', user_info=username, gist=gist, comments=comments, time_ago=time_ago)

    return render_template('index.html')

@app.route('/snippet/create', methods=['GET', 'POST'])
def create_snippet():
    if request.method == 'POST':
        # Form submission, create a new snippet
        description = request.form.get('description')
        filename = request.form.get('filename')
        code = request.form.get('code')

        create_gist(description, filename, code)

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

    return render_template('edit_snippet.html', snippet=snippet)

@app.route('/snippet/delete/<gist_id>')
def delete_snippet(gist_id):
    delete_gist(gist_id)
    return redirect(url_for('index'))

@app.route('/add_comment/<gist_id>', methods=['POST'])
def add_comment(gist_id):
    comment = request.form.get('comment')
    if comment:
        comment_gist(gist_id, comment)

    return redirect(url_for('snippet_detail', gist_id=gist_id))

@app.route('/delete_comment/<gist_id>/<comment_id>', methods=['POST'])
def delete_comment(gist_id, comment_id):
    comment_delete(gist_id, comment_id)

    return redirect(url_for('snippet_detail', gist_id=gist_id))