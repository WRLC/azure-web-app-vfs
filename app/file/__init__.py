"""
This is the credential package that contains the credential blueprint.
"""
from flask import Blueprint

bp = Blueprint('file', __name__, url_prefix='/file', template_folder='templates/file')  # Create the file blueprint
