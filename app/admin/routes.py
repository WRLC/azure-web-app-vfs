"""
This module is used to define the routes for the admin blueprint.
"""
from flask import render_template, abort, flash, redirect, url_for, Blueprint
from app.extensions import db, auth_required
from app.forms.admin_form import AdminForm
from app.models.admin import Admin

bp = Blueprint("admin", __name__, url_prefix='/admin')  # Create the admin blueprint


@bp.app_template_global()
@auth_required
def get_admins():
    """
    Get admins for Jinja2

    :return: list of admins
    """
    return Admin.get_admins()  # get the admins


@bp.route('/')
@auth_required
def index():
    """
    The index route for the admin blueprint.

    :return: The index page
    """
    return render_template(  # render the template
        'admin/index.html',  # template
        admins=Admin.get_admins(),  # get the admins
        title='Admins'  # title
    )


@bp.route('/new/', methods=['GET', 'POST'])
@auth_required
def new():
    """
    The new route for the admin blueprint.

    :return: The new page
    """
    form = AdminForm()  # create a new form

    return render_template(  # render the template
        'admin/form.html',  # template
        form=form,  # form
        title='Add Admin'  # title
    )


@bp.route('/<uid>/', methods=['GET', 'POST'])
@auth_required
def edit(uid):
    """
    The edit route for the admin blueprint.

    :param uid: admin UID
    :return: The edit page
    """
    admin = Admin.get_admin_by_uid(uid)  # get the admin

    if admin is None:  # if the admin does not exist
        abort(404)  # abort with a 404 error

    form = AdminForm(obj=admin)  # create a new form

    if form.validate_on_submit():  # if the form is submitted
        admin.uid = form.uid.data  # update the admin UID
        db.session.commit()  # commit the transaction

        flash('Admin updated successfully', 'success')  # show a success message

        return redirect(url_for('admin.index'))  # redirect to the admin page

    return render_template(  # render the template
        'admin/form.html',  # template
        admin=admin,  # admin
        form=form,  # form
        title='Edit Admin'  # title
    )


@bp.route('/<uid>/delete/', methods=['GET', 'POST'])
@auth_required
def delete(uid):
    """
    The delete route for the admin blueprint.

    :param uid: admin UID
    :return: The delete page
    """
    admin = Admin.get_admin_by_uid(uid)  # get the admin

    if admin is None:  # if the admin does not exist
        abort(404)  # abort with a 404 error

    return render_template(  # render the template
        'admin/delete.html',  # template
        admin=admin,  # admin
        title='Delete Admin'  # title
    )
