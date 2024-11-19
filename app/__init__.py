"""
Flask Application Factory
"""
from flask import Flask, Blueprint, session, redirect, url_for, render_template
from config import Config


def badrequest(e):
    """
    400 error handler

    :param e: error
    :return: 400 error template
    """
    return render_template('error_400.html', e=e), 400  # render the error template


def forbidden(e):
    """
    403 error handler

    :param e: error
    :return: 403 error template
    """
    return render_template('unauthorized.html', e=e), 403  # render the error template


def internalerror(e):
    """
    500 error handler

    :param e: error
    :return: 500 error template
    """
    return render_template('error_500.html', e=e), 500  # render the error template


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
    from app.file.routes import bp as file_bp
    application.register_blueprint(file_bp)  # Register the file blueprint

    from app.login.routes import bp as login_bp
    application.register_blueprint(login_bp)  # Register the login blueprint

    from app.admin.routes import bp as admin_bp
    application.register_blueprint(admin_bp)  # Register the admin blueprint

    # Register error handlers
    application.register_error_handler(400, badrequest)
    application.register_error_handler(403, forbidden)
    application.register_error_handler(500, internalerror)

    # App context
    # pylint: disable=wrong-import-position, import-outside-toplevel, unused-import
    from app.models import file, credential
    with application.app_context():
        db.create_all()  # Create the database tables

    return application
