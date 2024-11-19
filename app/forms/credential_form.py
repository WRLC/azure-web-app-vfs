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
    app_name = StringField('App Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
