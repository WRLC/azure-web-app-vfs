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
    credential_id = SelectField(  # credential field
        'App Credential',  # label
        coerce=int,  # coerce to int (the credential ID)
        description='The app credentials used for downloading the file',
        validators=[  # validators
            DataRequired(),  # required field
            NoneOf([0], message='Please select an app credential')  # not the default value
        ],
    )

    def __repr__(self):
        return f'<FileForm: {self.url.data}>'

    def __str__(self):
        return f'<FileForm: {self.url.data}>'
