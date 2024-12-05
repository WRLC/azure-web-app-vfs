"""
Flask Application Factory
"""
from flask import Flask, Blueprint, session, redirect, url_for, render_template  # noqa: F401
from app.admin import add_admin, remove_admin
from app.admin.routes import bp as admin_bp
from app.credential.routes import bp as credential_bp
from app.extensions import badrequest, forbidden, internalerror, db
from app.file.routes import bp as file_bp
from app.home.routes import bp as home_bp
from app.login.routes import bp as login_bp
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
    db.init_app(application)  # Initialize the database

    # Register blueprints here
    application.register_blueprint(home_bp)  # Register the home blueprint
    application.register_blueprint(login_bp)  # Register the login blueprint
    application.register_blueprint(file_bp)  # Register the file blueprint
    application.register_blueprint(credential_bp)  # Register the credential blueprint
    application.register_blueprint(admin_bp)  # Register the admin blueprint

    # Register error handlers
    application.register_error_handler(400, badrequest)
    application.register_error_handler(403, forbidden)
    application.register_error_handler(500, internalerror)

    # Create the database schema
    @application.cli.command('create_db')
    @with_appcontext
    def create_db():
        """
        Create the database

        :return: None
        """
        # pylint: disable=wrong-import-position, import-outside-toplevel, unused-import
        from app.models import file, credential, admin  # noqa: F401
        with application.app_context():
            db.create_all()  # Create the database tables
            print('Database created')

    application.cli.add_command(create_db)  # Add the create_db command
    application.cli.add_command(add_admin)  # Add the add_admin command
    application.cli.add_command(remove_admin)  # Add the remove_admin command

    @application.shell_context_processor
    def shell_context():
        """
        Shell context
        """
        return {'app': application, 'db': db}

    return application
