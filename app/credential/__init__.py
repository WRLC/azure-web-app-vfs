"""
This is the credential package that contains the credential blueprint.
"""
from flask import Blueprint

bp = Blueprint('credential', __name__, url_prefix='/credentials')
