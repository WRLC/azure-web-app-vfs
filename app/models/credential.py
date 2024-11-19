"""
Credential Class
"""
import os
from typing import List
from cryptography.fernet import Fernet
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class Credential(db.Model):
    """
    A class to represent a credential.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    files: Mapped[List["File"]] = relationship(back_populates='credential')

    def __repr__(self):
        return f'<Credential {self.username}>'

    @staticmethod
    def encrypt_pwd(pwd) -> bytes:
        """
        Encrypt password
        """
        key = os.getenv('FERNET_KEY')
        fernet = Fernet(key)
        return fernet.encrypt(pwd.encode())
