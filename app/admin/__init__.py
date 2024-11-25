"""
The admin blueprint is used to define the admin page of the application.
"""
import click
from flask import Blueprint, current_app
from flask.cli import with_appcontext, FlaskGroup
from app.extensions import db
from app.models.admin import Admin

bp = Blueprint("admin", __name__, url_prefix='/admin', template_folder='templates/admin')  # Create the admin blueprint

cli = FlaskGroup(create_app=current_app)  # type: ignore


@cli.command("add_admin")
@click.argument("uid")
@with_appcontext
def add_admin(uid):
    """
    Add an admin

    :param uid: admin UID
    :return: None
    """
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
    admin_user = Admin.get_admin_by_uid(uid)

    if not admin_user:
        print(f"Admin {uid} does not exist")
        return

    db.session.delete(admin_user)
    db.session.commit()

    print(f"Admin {uid} removed")
