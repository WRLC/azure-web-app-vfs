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
        session['username'] = self.user_data['UserName']  # set the username
        session['admin'] = self.user_admin(session)  # set the user's admin status

        return self

    @staticmethod
    def user_admin(session) -> bool:
        """
        Check if user is an admin

        :return:
        """
        if session['username'] in current_app.config['ADMINS']:  # if the username is in the admin list
            return True  # return True

        return False  # if the username is not in the admin list, return False
