"""
Admin routes
"""
from functools import wraps
from flask import session, current_app, redirect, url_for, Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')


def auth_required(f):
    """
    Decorator to require authentication

    :param f: original function's metadata
    :return: decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):  # the wrapper function
        if 'username' not in session:  # if the user is not logged in
            return redirect(url_for('login.login'))  # redirect to the login page
        return f(*args, **kwargs)  # otherwise, call the original function

    return decorated


@bp.route('/')
@auth_required
def admin():
    """
    Admin page

    :return: Admin page
    """
    if session['admin']:
        return 'Admin page'
    return current_app.forbidden("You are not an admin")


@bp.route('/files')
@auth_required
def admin_files():
    """
    Admin files page

    :return: Admin files page
    """
    if session['admin']:
        return 'Admin files page'
    return current_app.forbidden("You are not an admin")


@bp.route('/files/new/')
@auth_required
def admin_files_new():
    """
    Admin new file page

    :return: Admin new file page
    """
    if session['admin']:
        return 'Admin new file page'
    return current_app.forbidden("You are not an admin")


@bp.route('/files/<file_id>/')
@auth_required
def admin_files_edit(file_id):
    """
    Admin edit file page

    :return: Admin edit file page
    """
    if session['admin']:
        return 'Admin edit file page: ' + file_id
    return current_app.forbidden("You are not an admin")


@bp.route('/files/<file_id>/delete/')
@auth_required
def admin_files_delete(file_id):
    """
    Admin delete file page

    :return: Admin delete file page
    """
    if session['admin']:
        return 'Admin delete file page: ' + file_id
    return current_app.forbidden("You are not an admin")


@bp.route('/credentials')
@auth_required
def admin_credentials():
    """
    Admin credentials page

    :return: Admin credentials page
    """
    if session['admin']:
        return 'Admin credentials page'
    return current_app.forbidden("You are not an admin")
