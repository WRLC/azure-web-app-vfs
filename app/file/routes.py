"""
This is the main file for the Flask app.
"""
from flask import send_file, Blueprint, render_template, session, flash, redirect, url_for, request
from werkzeug.exceptions import Unauthorized
from app.extensions import auth_required, forbidden, db, internalerror
from app.forms.file_form import FileForm
from app.models.credential import Credential
from app.models.file import File

bp = Blueprint('file', __name__, url_prefix='/files')  # Create the file blueprint


@bp.route('/')
@auth_required
def index():
    """
    Home page

    :return: List of file to download
    """
    return render_template(
        'file/index.html',
        files=sorted(File.get_files(), key=lambda x: x.get_filename()),
        credentials=sorted(Credential.get_credentials(), key=lambda x: x.app_name),
        title='Files'
    )


@bp.route('/<file_id>/')
@auth_required
def download(file_id):
    """
    Download handler

    :return: file to download
    """
    file = File.get_file_by_id(file_id)  # get the file
    file_path = file.download_file()  # download the file

    if isinstance(file_path, Exception):  # if the file download fails
        flash('Failed to download file', 'danger')
        if file_path.response.status_code == 403:
            return forbidden(file_path)
        return internalerror(file_path.response.status_code)  # return a 500 error

    return send_file(file_path, download_name=file.get_filename())  # send the file


@bp.route('/new', methods=['GET', 'POST'])
@auth_required
def new_file():
    """
    Add new file

    :return: Add new file page
    """
    if session['admin']:  # if the user is an admin

        form = FileForm()  # create a new form
        credentials = sorted(Credential.get_credentials(), key=lambda x: x.app_name)  # get the credentials
        options = [(c.id, c.app_name) for c in credentials]  # set the credential choices
        options.insert(0, (0, '--- Select an app credential ---'))  # add a default option
        form.credential_id.choices = options  # set credential choices

        if form.validate_on_submit():  # if the form is submitted

            db.session.add(  # add the new file to the database
                File(  # create a new file object
                    url=form.url.data,  # url
                    credential_id=form.credential_id.data  # credential id
                )
            )

            db.session.commit()  # commit the transaction

            flash('File added successfully', 'success')  # show a success message

            return redirect(url_for('file.index'))  # redirect to the file page

        return render_template(  # if the form is not submitted, render the form
            'file/form.html',  # template
            form=form,  # form
            credentials=credentials,  # credentials
            title='Add File'  # title
        )

    return render_template('file/new.html')


@bp.route('<file_id>/edit', methods=['GET', 'POST'])
@auth_required
def edit_file(file_id):
    """
    Edit file

    :return: Edit file page
    """
    if session['admin']:  # if the user is an admin

        file = File.get_file_by_id(file_id)  # get the file

        form = FileForm(obj=file)  # create a form object with the file data
        credentials = sorted(Credential.get_credentials(), key=lambda x: x.app_name)  # get the credentials
        options = [(c.id, c.app_name) for c in credentials]  # set the credential choices
        options.insert(0, (0, '--- Select an app credential ---'))  # add a default option
        form.credential_id.choices = options  # set credential choices

        if form.validate_on_submit():  # if the form is submitted, update the file

            file.url = form.url.data  # url
            file.credential_id = form.credential_id.data  # credential id

            db.session.commit()  # commit the transaction

            flash('File updated successfully', 'success')  # show a success message

            return redirect(url_for('file.index'))  # redirect to the file page

        return render_template(  # if the form is not submitted, render the form
            'file/form.html',  # template
            form=form,  # form
            file=file,  # file
            credentials=credentials,  # credentials
            title='Edit File'  # title
        )

    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error


@bp.route('<file_id>/delete', methods=['GET', 'POST'])
@auth_required
def delete_file(file_id):
    """
    Delete file

    :return: Delete file page
    """
    if session['admin']:  # if the user is an admin

        file = File.get_file_by_id(file_id)  # get the file

        if request.method == 'POST':  # if the form is submitted

            db.session.delete(file)  # delete the file
            db.session.commit()  # commit the transaction

            flash('File deleted successfully', 'success')  # show a success message

            return redirect(url_for('file.index'))  # redirect to the file page

        return render_template(  # if the form is not submitted, render the form
            'file/delete.html',  # template
            file=file,  # file
            title='Delete File'  # title
        )

    return forbidden("You are not an admin")  # if the user is not an admin, return a 403 error
