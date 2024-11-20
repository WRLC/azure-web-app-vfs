"""
This file contains the form for the File model.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL, NoneOf


class FileForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """
    File form
    """
    url = StringField(  # URL field
        'File URL',  # label
        description='The Azure Kudo VFS API URL (found in the resource\'s "Advanced Tools"',  # description
        validators=[  # validators
            DataRequired(),  # required field
            URL()  # URL validator
        ]
    )
    credential_id = SelectField(  # credential field
        'App Credential',  # label
        coerce=int,  # coerce to int (the credential ID)
        description='The app credentials used for downloading the file',
        validators=[  # validators
            DataRequired(),  # required field
            NoneOf([0], message='Please select an app credential')  # not the default value
        ],
    )
