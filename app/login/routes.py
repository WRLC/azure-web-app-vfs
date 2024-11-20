"""
Routes for the login blueprint
"""
from pymemcache.client.base import Client as memcacheClient  # type: ignore
from flask import current_app, redirect, request, session, url_for, Blueprint
from app.models.login import Login

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/')
def login():
    """
    Login page

    :return: Login form
    """
    saml_sp = current_app.config['SAML_SP']  # Get SAML SP URL
    cookie_file = current_app.config['COOKIE_ISSUING_FILE']  # Get cookie issuing file
    slug = current_app.config['SERVICE_SLUG']  # Get service slug
    return redirect(saml_sp + cookie_file + '?service=' + slug)  # Redirect to SAML SP


@bp.route('/n/', methods=['GET'])
def new_login():
    """
    Login handler

    :return: redirect to the home page
    """
    cookie_name = current_app.config['COOKIE_PREFIX'] + current_app.config['SERVICE_SLUG']
    session.clear()  # clear the session
    if cookie_name in request.cookies:  # if the login cookie is present
        memcached_key = request.cookies[cookie_name]  # get the login cookie
        memcached = memcacheClient((current_app.config['MEMCACHED_SERVER'], current_app.config['MEMCACHED_PORT']))

        user_data = {}

        try:
            user = memcached.get(memcached_key, False).decode('utf-8').splitlines()
        except AttributeError:
            return "no login session"

        if not user:
            return "no login session"

        for line in user:
            key, value = line.split('=')
            user_data[key] = value

        user_login = Login(user_data)
        user_login.user_login(session=session)  # Log the user in

        return redirect(url_for('file.hello_world'))

    return "no login cookie"  # if the login cookie is not present, return an error
