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

    def user_login(self, session: SessionMixin):
        """
        Log the user in

        :param session:
        :return:
        """
        session['username']: str = self.user_data['UserName']  # Set the username
        session['admin'] = self.user_admin(session)

        return self

    @staticmethod
    def user_admin(session) -> bool:
        """
        Check if user is an admin

        :return:
        """
        if session['username'] in current_app.config['ADMINS']:
            return True

        return False
