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
