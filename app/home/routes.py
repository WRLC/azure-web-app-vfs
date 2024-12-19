"""
Home routes
"""
from flask import session, redirect, current_app, url_for, Blueprint
from app.extensions import auth_required

bp = Blueprint('home', __name__)  # Create the home blueprint


@bp.route('/')
@auth_required
def index():
    """
    Home page

    :return: Redirect to the file index
    """
    return redirect(url_for('resource.index'))  # redirect to the file index


@bp.route('/logout/')
@auth_required
def logout():
    """
    Logout handler

    :return: redirect to the logout script
    """
    session.clear()  # clear the session
    return redirect(  # redirect to the SP logout script
        current_app.config['SAML_SP'] +  # SAML SP URL
        current_app.config['LOGOUT_SCRIPT'] +  # logout script
        '?service=' +
        current_app.config['SERVICE_SLUG']  # service slug
    )
