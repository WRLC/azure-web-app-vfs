"""
This file contains the form for the File model.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """
    File form
    """
    name = StringField('Name', validators=[DataRequired()])
    filename = StringField('Filename', validators=[DataRequired()])
    credential_id = SelectField('Credential', coerce=int, validators=[DataRequired()])
