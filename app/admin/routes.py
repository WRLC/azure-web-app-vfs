"""
This module is used to define the routes for the admin blueprint.
"""
from app.admin import bp
from app.models.admin import Admin


@bp.app_template_global()
def get_admins():
    """
    Get admins for Jinja2

    :return: list of admins
    """
    return Admin.get_admins()


@bp.route('/')
def index():
    """
    The index route for the admin blueprint.

    :return: The index page
    """
    return 'Admin Index'
