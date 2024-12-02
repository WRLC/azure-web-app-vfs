"""
Admin routes
"""
from flask import session, redirect, url_for, render_template, flash, request
from app.credential import bp
from app.extensions import db, forbidden, auth_required
from app.models.admin import Admin
from app.models.credential import Credential
from app.forms.credential_form import CredentialForm


@bp.route('/')
@auth_required
def index():
    """
    App credentials landing page

    :return: App credentials landing page
    """
    if session['username'] in Admin.get_admins():  # if the user is an admin

        return render_template(  # render the credential page
            'credential/index.html',  # template
            credentials=sorted(Credential.get_credentials(), key=lambda x: x.app_name),  # credential
            title='App Credentials'  # title
        )

    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('/new/', methods=['GET', 'POST'])
@auth_required
def credentials_new():
    """
    Add app credential

    :return: Add app credential page
    """
    if session['username'] in Admin.get_admins():  # if the user is an admin

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

            return redirect(url_for('credential.credentials'))  # redirect to the credential page

        return render_template(  # if the form is not submitted, render the form
            'credential/form.html',  # template
            form=form,  # form
            title='Add App Credential'  # title
        )

    return forbidden("You are not an admin.")  # if the user is not an admin, return a 403 error


@bp.route('/<credential_id>/', methods=['GET', 'POST'])
@auth_required
def credentials_edit(credential_id):
    """
    Edit app credential

    :return: Edit app credential page
    """
    if session['username'] in Admin.get_admins():  # if the user is an admin

        credential = Credential.get_credential_by_id(credential_id)  # get the credential by id
        form = CredentialForm(obj=credential)  # create a form with the credential data

        if form.validate_on_submit():  # if the form is submitted, update the credential

            credential.app_name = form.app_name.data  # app name
            credential.username = form.username.data  # username
            credential.password = form.password.data  # password

            db.session.commit()  # commit the transaction

            flash('Credential updated successfully', 'success')  # show a success message

            return redirect(url_for('credential.credentials'))  # redirect to the credential page

        return render_template(  # if the form is not submitted, render the form
            'credential/form.html',  # template
            form=form,  # form
            title='Edit App Credential'  # title
        )

    return forbidden("You are not an admin.")  # if the user is not an admin, return a 403 error


@bp.route('/<credential_id>/delete/', methods=['GET', 'POST'])
@auth_required
def credentials_delete(credential_id):
    """
    Delete app credential

    :return: Delete app credential page
    """
    if session['username'] in Admin.get_admins():  # if the user is an admin

        credential = Credential.get_credential_by_id(credential_id)  # get the credential by id

        if request.method == 'POST':  # if the form is submitted

            db.session.delete(credential)  # delete the credential
            db.session.commit()  # commit the transaction

            flash('Credential deleted successfully', 'success')  # show a success message

            return redirect(url_for('credential.credentials'))  # redirect to the credential page

        return render_template(  # if the form is not submitted, render the form
            'credential/delete.html',  # template
            credential=credential,  # credential
            title='Delete App Credential'  # title
        )

    return forbidden("You are not an admin.")  # if the user is not an admin, return a 403 error
