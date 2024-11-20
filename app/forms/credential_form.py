"""
This file contains the form for the credential model.
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class CredentialForm(FlaskForm):
    """
    Credential form
    """
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
        return f'<CredentialForm: {self.app_name.data}>'

    def __str__(self):
        return f'<CredentialForm: {self.app_name.data}>'
