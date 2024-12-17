from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model  # pylint: disable=ungrouped-imports
else:
    Model = db.Model


class Resource(Model):
    """
    Resource class
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    app_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'<Resource: {self.app_name}>'

    def __str__(self):
        return f'<Resource: {self.app_name}>'
