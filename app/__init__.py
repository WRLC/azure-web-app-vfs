"""
Flask Application Factory
"""
import click
from flask import Flask
from flask.cli import with_appcontext, FlaskGroup
from app.extensions import badrequest, forbidden, internalerror, db
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
    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.home import bp as home_bp  # noqa: F401
    application.register_blueprint(home_bp)  # Register the home blueprint

    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.login import bp as login_bp  # noqa: F401
    application.register_blueprint(login_bp)  # Register the login blueprint

    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.admin import bp as admin_bp  # noqa: F401
    application.register_blueprint(admin_bp)  # Register the admin blueprint

    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.resource import bp as resource_bp  # noqa: F401
    application.register_blueprint(resource_bp)  # Register the resource blueprint

    # Register error handlers
    application.register_error_handler(400, badrequest)
    application.register_error_handler(403, forbidden)
    application.register_error_handler(500, internalerror)

    # Register the CLI commands
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


cli = FlaskGroup(create_app=create_app)  # Create the CLI


# Create the database schema
@cli.command('create_db')
@with_appcontext
def create_db():
    """
    Create the database

    :return: None
    """
    # pylint: disable=wrong-import-position, import-outside-toplevel, unused-import
    from app.models import admin, resource  # noqa: F401
    db.create_all()  # Create the database tables
    print('Database created')


@cli.command("add_admin")
@click.argument("uid")
@with_appcontext
def add_admin(uid):
    """
    Add an admin

    :param uid: admin UID
    :return: None
    """
    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.models.admin import Admin  # noqa: F401
    admin_user = Admin.get_admin_by_uid(uid)

    if admin_user:
        print(f"Admin {uid} already exists")
        return

    admin_user = Admin(uid=uid)
    db.session.add(admin_user)
    db.session.commit()

    print(f"Admin {uid} added")


@cli.command("remove_admin")
@click.argument("uid")
@with_appcontext
def remove_admin(uid):
    """
    Remove an admin

    :param uid: admin UID
    :return: None
    """
    # pylint: disable=wrong-import-position, import-outside-toplevel
    from app.models.admin import Admin  # noqa: F401
    admin_user = Admin.get_admin_by_uid(uid)

    if not admin_user:
        print(f"Admin {uid} does not exist")
        return

    db.session.delete(admin_user)
    db.session.commit()

    print(f"Admin {uid} removed")
