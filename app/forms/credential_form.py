"""
This file contains the form for the credential model.
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


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
