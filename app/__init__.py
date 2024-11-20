"""
Flask Application Factory
"""
import os.path

from flask import Flask, Blueprint, session, redirect, url_for, render_template
from config import Config


def create_app(config_class=Config):
    """
    Create the Flask app

    :param config_class: configuration class
    :return: Flask app
    """
    application = Flask(__name__)  # Create the Flask app
    application.config.from_object(config_class)  # Load the configuration file

    # Initialize Flask extensions here
    # pylint: disable=import-outside-toplevel
    from app.extensions import db
    db.init_app(application)  # Initialize the database

    # Register blueprints here
    # pylint: disable=import-outside-toplevel
    from app.home.routes import bp as home_bp
    application.register_blueprint(home_bp)  # Register the home blueprint

    from app.login.routes import bp as login_bp
    application.register_blueprint(login_bp)  # Register the login blueprint

    from app.file.routes import bp as file_bp
    application.register_blueprint(file_bp)  # Register the file blueprint

    from app.credential.routes import bp as credential_bp
    application.register_blueprint(credential_bp)  # Register the credential blueprint

    # Register error handlers
    from app.extensions import badrequest, forbidden, internalerror
    application.register_error_handler(400, badrequest)
    application.register_error_handler(403, forbidden)
    application.register_error_handler(500, internalerror)

    @application.template_filter('basename_filter')
    def basename_filter(path):
        """
        Base name filter for Jinja2

        :param path: path
        :return: base name
        """
        return os.path.basename(path)

    # App context
    # pylint: disable=wrong-import-position, import-outside-toplevel, unused-import
    from app.models import file, credential
    with application.app_context():
        db.create_all()  # Create the database tables

    return application
