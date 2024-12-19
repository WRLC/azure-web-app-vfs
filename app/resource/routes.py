"""
Routes for the resource blueprint
"""
import json
from email.policy import default

from flask import Blueprint, render_template, flash, redirect, abort, url_for, request, send_file
from app.extensions import auth_required, db
from app.forms.resource_form import ResourceForm
from app.models.resource import Resource

bp = Blueprint('resource', __name__, url_prefix='/resource')  # Create the file blueprint


@bp.route('/')
@auth_required
def index():
    """
    Index page for the resource blueprint

    :return: render_template
    """
    return render_template(  # Render the template
        'resource/index.html',  # Template
        resources=Resource.get_all(),  # Get all resources
        title='Resources'  # Title
    )


@bp.route('/new/', methods=['GET', 'POST'])
@auth_required
def new():
    """
    New page for the resource blueprint

    :return: render_template
    """
    form = ResourceForm()  # Create a new form

    if form.validate_on_submit():  # If the form is submitted

        resource = Resource(  # Create a new resource
            app_name=form.app_name.data,   # App name
            app_description=form.app_description.data,  # App description
            url=form.url.data,  # URL
            username=form.username.data,  # Username
            password=form.password.data  # Password
        )

        db.session.add(resource)  # Add the resource to the database
        db.session.commit()  # Commit the changes

        flash(f'New Resource: {resource.app_name}', 'success')  # Flash a success message

        return redirect(url_for('resource.index'))  # Redirect to the index page

    return render_template(  # Render the template
        'resource/form.html',  # Template
        form=form,  # Form
        title='Add Resource'  # Title
    )


@bp.route('/<int:resource_id>')
@auth_required
def view(resource_id):
    """
    View page for the resource blueprint

    :param resource_id: resource ID
    :return: render_template
    """
    resource = Resource.get_by_id(resource_id)  # Get the resource

    if resource is None:  # If the resource does not exist
        abort(404)  # Abort with a 404 error

    path = request.args.get('path').strip('/') if request.args.get('path') else ''  # Get the path from the request

    objects = resource.get_files_by_path(path=path)  # Get the files by path

    if objects is type(Exception):  # If the objects are an exception
        abort(404)  # Abort with a 404 error

    folders = []  # Folders
    files = []  # Files

    for fileobject in objects.json():  # Loop through the objects
        if fileobject['mime'] == 'inode/directory':  # If the object is a directory
            folders.append(fileobject)  # Append the object to the folders
        else:  # If the object is a file
            files.append(fileobject)  # Append the object to the files

    return render_template(  # Render the template
        'resource/view.html',  # Template
        resource=resource,  # Resource
        path=path.split('/'),  # Path
        folders=folders,  # Folders
        files=files,  # Files
        title=f'{path}'  # Title
    )


@bp.route('/<int:resource_id>/download')
@auth_required
def download(resource_id):
    """
    Download page for the resource blueprint

    :param resource_id: resource ID
    :return: render_template
    """
    resource = Resource.get_by_id(resource_id)

    if resource is None:
        abort(404)

    path = request.args.get('path') if request.args.get('path') else ''

    file = resource.download_file(path=path)

    if isinstance(file, Exception):  # if the file download fails
        abort(404)  # return a 404 error

    return send_file(file, download_name=resource.get_filename(file))  # send the file


@bp.route('/<int:resource_id>/edit/', methods=['GET', 'POST'])
@auth_required
def edit(resource_id):
    """
    View page for the resource blueprint

    :param resource_id: resource ID
    :return: render_template
    """
    resource = Resource.get_by_id(resource_id)  # Get the resource

    if resource is None:  # If the resource does not exist
        abort(404)  # Abort with a 404 error

    form = ResourceForm(obj=resource)  # Create a new form

    if form.validate_on_submit():  # If the form is submitted, update the resource
        resource.app_name = form.app_name.data  # App name
        resource.url = form.url.data  # URL
        resource.username = form.username.data  # Username
        resource.password = form.password.data  # Password

        db.session.commit()  # Commit the changes

        flash(f'Resource updated: {resource.app_name}', 'success')  # Flash a success message

        return redirect(url_for('resource.view', resource_id=resource.id))  # Redirect to the resource page

    return render_template(  # Render the template
        'resource/form.html',  # Template
        resource=resource,  # Resource
        form=form,  # Form
        title='Edit Resource'  # Title
    )


@bp.route('/<int:resource_id>/delete/', methods=['GET', 'POST'])
@auth_required
def delete(resource_id):
    """
    Delete page for the resource blueprint

    :param resource_id: resource ID
    :return: render_template
    """
    resource = Resource.get_by_id(resource_id)

    if resource is None:
        abort(404)

    return f'Delete Resource {resource_id}'
