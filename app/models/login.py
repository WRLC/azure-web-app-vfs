"""
Login model
"""
from flask.sessions import SessionMixin
from app.models.admin import Admin


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
        session['admin'] = Admin.is_admin(self.user_data['UserName'])  # set the user's admin status

        return self
