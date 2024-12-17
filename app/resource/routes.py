"""
Routes for the resource blueprint
"""
from flask import Blueprint
from app.extensions import auth_required

bp = Blueprint('resource', __name__, url_prefix='/resource')  # Create the file blueprint


@bp.route('/')
@auth_required
def index():
    """
    Index page for the resource blueprint

    :return: render_template
    """
    return 'Resource'
