"""
Admin form
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class AdminForm(FlaskForm):
    """
    Admin form
    """
    uid = StringField(  # uid field
        'UID',  # label
        description='The admin\'s UID',  # description
        validators=[DataRequired()]  # required field
    )

    def __repr__(self):
        return f'<AdminForm: {self.uid.data}>'
