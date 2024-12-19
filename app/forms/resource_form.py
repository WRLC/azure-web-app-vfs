"""
This file contains the form for the File model.
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField  # type: ignore
from wtforms.validators import DataRequired, URL  # type: ignore


class ResourceForm(FlaskForm):
    """
    File form
    """
    app_name = StringField(  # app name field
        'Name',  # label
        description='The Azure resource\'s name',  # description
        validators=[DataRequired()]  # required field
    )
    app_description = StringField(  # app description field
        'Description',  # label
        description='A brief description of the Azure resource',  # description
    )
    url = StringField(  # URL field
        'API URL',  # label
        description='The Azure Kudo VFS API URL (found in the resource\'s "Advanced Tools")',  # description
        validators=[  # validators
            DataRequired(),  # required field
            URL()  # URL validator
        ]
    )
    username = StringField(  # username field
        'Username',  # label
        description='Probably the FTPS username from the resource\'s Deployment Center',  # description
        validators=[DataRequired()]  # required field
    )
    password = StringField(  # password field
        'Password',  # label
        description='Probably the FTPS password from the resource\'s Deployment Center',  # description
        validators=[DataRequired()]  # required field
    )

    def __repr__(self):
        return f'<FileForm: {self.url.data}>'

    def __str__(self):
        return f'<FileForm: {self.url.data}>'
