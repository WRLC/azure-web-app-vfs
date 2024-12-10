"""
The admin blueprint is used to define the admin page of the application.
"""
from flask import Blueprint

bp = Blueprint("admin", __name__, url_prefix='/admin', template_folder='templates/admin')  # Create the admin blueprint
