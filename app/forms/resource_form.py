"""
This file contains the form for the File model.
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SelectField  # type: ignore
from wtforms.validators import DataRequired, URL, NoneOf  # type: ignore


class FileForm(FlaskForm):
    """
    File form
    """
    url = StringField(  # URL field
        'File URL',  # label
        description='The Azure Kudo VFS API URL (found in the resource\'s "Advanced Tools")',  # description
        validators=[  # validators
            DataRequired(),  # required field
            URL()  # URL validator
        ]
    )
    app_name = StringField(  # app name field
        'App Name',  # label
        description='Ideally the Azure resource\'s name (to easily identify the app)',  # description
        validators=[DataRequired()]  # required field
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
