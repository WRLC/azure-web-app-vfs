"""
This file contains the extensions that will be used in the application.
"""
from functools import wraps
from flask import render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create a database object


def badrequest(e):
    """
    400 error handler

    :param e: error
    :return: 400 error template
    """
    return render_template('error/error_400.html', e=e), 400  # render the error template


def forbidden(e):
    """
    403 error handler

    :param e: error
    :return: 403 error template
    """
    return render_template('error/unauthorized.html', e=e), 403  # render the error template


def internalerror(e):
    """
    500 error handler

    :param e: error
    :return: 500 error template
    """
    return render_template('error/error_500.html', e=e), 500  # render the error template


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
