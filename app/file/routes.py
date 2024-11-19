"""
This is the main file for the Flask app.
"""
from functools import wraps
from flask import session, redirect, url_for, current_app, send_file, Blueprint
from app.models.file import File

bp = Blueprint('file', __name__)


def auth_required(f):
    """
    Decorator to require authentication

    :param f: original function's metadata
    :return: decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):  # the wrapper function
        """
        Wrapper function

        :param args:
        :param kwargs:
        :return: decorated function
        """
        if 'username' not in session:  # if the user is not logged in
            return redirect(url_for('login.login'))  # redirect to the login page
        return f(*args, **kwargs)  # otherwise, call the original function

    return decorated


@bp.route('/')
@auth_required
def hello_world():
    """
    Home page

    :return: List of files to download
    """
    return 'Hello World!'


@bp.route('/logout/')
@auth_required
def logout():
    """
    Logout handler

    :return: redirect to the logout script
    """
    session.clear()  # clear the session
    return redirect(
        current_app.config['SAML_SP'] +
        current_app.config['LOGOUT_SCRIPT'] +
        '?service=' +
        current_app.config['SERVICE_SLUG']
    )  # redirect to the logout script


@bp.route('/<file_id>/')
@auth_required
def download(file_id):
    """
    Download handler

    :return: file to download
    """
    file = File.get_file(file_id)

    return send_file(file.download_file())
