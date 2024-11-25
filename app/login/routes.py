"""
Routes for the login blueprint
"""
from pymemcache.client.base import Client as memcacheClient  # type: ignore
from flask import current_app, redirect, request, session, url_for
from app.login import bp
from app.models.login import Login


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
    cookie_name = current_app.config['COOKIE_PREFIX'] + current_app.config['SERVICE_SLUG']  # Get the cookie name
    session.clear()  # clear the session
    if cookie_name in request.cookies:  # if the login cookie is present
        memcached_key = request.cookies[cookie_name]  # get the login cookie
        memcached = memcacheClient(  # connect to memcached
            (current_app.config['MEMCACHED_SERVER'], current_app.config['MEMCACHED_PORT'])  # memcached server and port
        )

        user_data = {}  # user data dictionary

        try:
            user = memcached.get(memcached_key, False).decode('utf-8').splitlines()  # get the user data
        except AttributeError:
            return "no login session"  # if this returns an error...return an error message

        if not user:
            return "no login session"  # if the user object isn't present, return an error message

        for line in user:  # for each line in the user object
            key, value = line.split('=')  # split the line into key and value
            user_data[key] = value  # add the key and value to the user data dictionary

        user_login = Login(user_data)  # create a new login object
        user_login.user_login(session=session)  # Log the user in

        return redirect(url_for('file.index'))  # Redirect to the home page

    return "no login cookie"  # if the login cookie is not present, return an error
