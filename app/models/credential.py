"""
Credential Class
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model  # pylint: disable=ungrouped-imports
else:
    Model = db.Model


class Credential(Model):
    """
    A class to represent a credential.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    app_name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    files: Mapped[List["File"]] = relationship(back_populates='credential')  # type: ignore # noqa: F821

    def __repr__(self):
        return f'<Credential {self.username}>'

    @staticmethod
    def get_credentials():
        """
        Get credential
        """
        return db.session.execute(
            db.select(Credential)
        ).scalars().all()

    @staticmethod
    def get_credential_by_id(credential_id):
        """
        Get a credential by id
        """
        return db.session.execute(
            db.select(Credential).where(Credential.id == credential_id)
        ).scalar_one()
