"""
Admin model
"""
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model  # pylint: disable=ungrouped-imports
else:
    Model = db.Model


class Admin(Model):
    """
    Admin model
    """
    __tablename__ = 'admin'
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Admin('{self.uid}')"

    @staticmethod
    def get_admins():
        """
        Get admins
        """
        admins = db.session.execute(
            db.select(Admin)
        ).scalars().all()

        return [admin.uid for admin in admins]

    @staticmethod
    def get_admin_by_uid(uid):
        """
        Get an admin by id
        """
        return db.session.execute(
            db.select(Admin).where(Admin.uid == uid)
        ).scalar_one_or_none()

    @staticmethod
    def is_admin(uid):
        """
        Check if a user is an admin
        """
        admin_uid = db.session.execute(  # get the admin UID
            db.select(Admin).where(Admin.uid == uid)
        ).scalar_one_or_none()

        if admin_uid is None:  # if the admin UID exists, return True
            return False

        return False  # if the admin UID does not exist, return False
