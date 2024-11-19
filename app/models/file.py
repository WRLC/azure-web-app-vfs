"""
File class
"""
import os
from typing import BinaryIO
from base64 import b64encode
from cryptography.fernet import Fernet
import requests
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class File(db.Model):
    """
    File class
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    credential_id: Mapped[int] = mapped_column(ForeignKey('credential.id'), nullable=False)
    credential: Mapped["Credential"] = relationship(back_populates='file')

    def __repr__(self):
        return f'<File {self.name}>'

    def download_file(self) -> BinaryIO:
        """
        Download file
        """
        base64_auth_info = b64encode(  # encode the username and password
            (self.credential.username + ':' + self.decrypt_pwd(
                self.credential.password
            )).encode('ascii')
        ).decode('ascii')

        headers = {'Authorization': 'Basic ' + base64_auth_info}  # create the authz header

        response = requests.get(url=self.url, headers=headers, timeout=60)  # make the request

        with open('tmp/almarsa_psb.log', 'wb') as f:  # write the response to a file
            f.write(response.content)

        return f

    @staticmethod
    def get_file(file_id):
        """
        Get file
        """
        return db.session.execute(
            db.select(File).filter(File.id == file_id)
        ).scalar_one()

    @staticmethod
    def decrypt_pwd(pwd) -> str:
        """
        Decrypt password
        """
        key = os.getenv('FERNET_KEY')
        fernet = Fernet(key)
        return fernet.decrypt(pwd).decode()
