"""
The home blueprint is used to define the home page of the application.
"""
import os
from flask import Blueprint

bp = Blueprint('home', __name__)  # Create the home blueprint


@bp.app_template_filter('basename_filter')
def basename_filter(path):
    """
    Base name filter for Jinja2

    :param path: path
    :return: base name
    """
    return os.path.basename(path)
