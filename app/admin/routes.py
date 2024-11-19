"""
Admin routes
"""
from functools import wraps
from flask import session, redirect, url_for, Blueprint, render_template, flash, request
from app import forbidden
from app.extensions import db
from app.forms.file_form import FileForm
from app.models.file import File
from app.models.credential import Credential
from app.forms.credential_form import CredentialForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


def auth_required(f):
    """
    Decorator to require authentication

    :param f: original function's metadata
    :return: decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):  # the wrapper function
        if 'username' not in session:  # if the user is not logged in
            return redirect(url_for('login.login'))  # redirect to the login page
        return f(*args, **kwargs)  # otherwise, call the original function

    return decorated


@bp.route('/')
@auth_required
def admin():
    """
    Admin landing page

    :return: Admin landing page
    """
    if session['admin']:  # if the user is an admin
        return render_template(  # render the admin page
            'admin/index.html',  # template
            title='Admin'  # title
        )
    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/files')
@auth_required
def admin_files():
    """
    Files admin landing page

    :return: Files admin landing page
    """
    if session['admin']:  # if the user is an admin
        return render_template(  # render the files page
            'admin/files/index.html',  # template
            files=File.get_files(),  # files
            title='Files'  # title
        )
    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/files/new/', methods=['GET', 'POST'])
@auth_required
def admin_files_new():
    """
    Add new file

    :return: Admin new file page
    """
    if session['admin']:
        form = FileForm()
        if form.validate_on_submit():

            return redirect(url_for('admin.admin_files'))

        return render_template(
            'admin/files/form.html',
            form=form,
            credentials=Credential.get_credentials(),
            title='Add New File'
        )
    return forbidden("You are not an admin")


@bp.route('/files/<file_id>/')
@auth_required
def admin_files_edit(file_id):
    """
    Edit a file

    :return: Admin edit file page
    """
    if session['admin']:
        return 'Admin edit file page: ' + file_id
    return forbidden("You are not an admin")


@bp.route('/files/<file_id>/delete/')
@auth_required
def admin_files_delete(file_id):
    """
    Delete a file

    :return: Admin delete file page
    """
    if session['admin']:
        return 'Admin delete file page: ' + file_id
    return forbidden("You are not an admin")


@bp.route('/credentials')
@auth_required
def admin_credentials():
    """
    Credentials admin landing page

    :return: Credentials admin landing page
    """
    if session['admin']:  # if the user is an admin
        return render_template(  # render the credentials page
            'admin/credentials/index.html',  # template
            credentials=Credential.get_credentials(),  # credentials
            title='App Credentials'  # title
        )
    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/credentials/new/', methods=['GET', 'POST'])
@auth_required
def admin_credentials_new():
    """
    Add new credential

    :return: Add new credential page
    """
    if session['admin']:  # if the user is an admin
        form = CredentialForm()  # create a new form

        if form.validate_on_submit():  # if the form is submitted
            db.session.add(  # add the new credential to the database
                Credential(  # create a new credential object
                    app_name=form.app_name.data,  # app name
                    username=form.username.data,  # username
                    password=form.password.data  # password
                )
            )
            db.session.commit()  # commit the transaction

            flash('Credential added successfully', 'success')  # show a success message

            return redirect(url_for('admin.admin_credentials'))  # redirect to the credentials page

        return render_template(  # if the form is not submitted, render the form
            'admin/credentials/form.html',  # template
            form=form,  # form
            title='Add new App Credential'  # title
        )
    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/credentials/<credential_id>/', methods=['GET', 'POST'])
@auth_required
def admin_credentials_edit(credential_id):
    """
    Edit a credential

    :return: Edit a credential page
    """
    if session['admin']:  # if the user is an admin
        credential = Credential.get_credential_by_id(credential_id)  # get the credential by id
        form = CredentialForm(obj=credential)  # create a form with the credential data

        if form.validate_on_submit():  # if the form is submitted, update the credential
            credential.app_name = form.app_name.data  # app name
            credential.username = form.username.data  # username
            credential.password = form.password.data  # password

            db.session.commit()  # commit the transaction

            flash('Credential updated successfully', 'success')  # show a success message

            return redirect(url_for('admin.admin_credentials'))  # redirect to the credentials page

        return render_template(  # if the form is not submitted, render the form
            'admin/credentials/form.html',  # template
            form=form,  # form
            title='Edit App Credential'  # title
        )
    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/credentials/<credential_id>/delete/', methods=['GET', 'POST'])
@auth_required
def admin_credentials_delete(credential_id):
    """
    Delete a credential

    :return: Admin delete credential page
    """
    if session['admin']:
        credential = Credential.get_credential_by_id(credential_id)
        if request.method == 'POST':
            db.session.delete(credential)
            db.session.commit()
            flash('Credential deleted successfully', 'success')
            return redirect(url_for('admin.admin_credentials'))
        return render_template('admin/credentials/delete.html', credential=credential)
    return forbidden("You are not an admin")
