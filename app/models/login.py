"""
Login model
"""
from flask import current_app
from flask.sessions import SessionMixin


class Login:
    """
    Login model
    """
    def __init__(self, user_data: dict):
        self.user_data = user_data

    def __repr__(self):
        return f"Login('{self.user_data['username']}')"

    def user_login(self, session: SessionMixin):
        """
        Log the user in

        :param session:
        :return:
        """
        session['username']: str = self.user_data['username']  # Set the username
        session['admin'] = self.user_admin()

        return self

    def user_admin(self) -> bool:
        """
        Check if user is an admin

        :return:
        """
        if self.user_data['username'] in current_app.config['ADMINS']:
            return True

        return False
