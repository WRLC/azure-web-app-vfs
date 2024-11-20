"""
File class
"""
import os.path
from base64 import b64encode
from typing import TYPE_CHECKING
import requests  # type: ignore
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model  # pylint: disable=ungrouped-imports
else:
    Model = db.Model


class File(Model):
    """
    File class
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    credential_id: Mapped[int] = mapped_column(ForeignKey('credential.id'), nullable=False)
    credential: Mapped["Credential"] = relationship(back_populates='files')  # type: ignore # noqa: F821

    def get_filename(self) -> str:
        """
        Get file name from URL
        """
        return os.path.basename(self.url)

    def download_file(self) -> str | Exception:
        """
        Download file
        """
        base64_auth_info = b64encode(  # encode the username and password
            (self.credential.username + ':' + self.credential.password).encode('ascii')
        ).decode('ascii')

        headers = {'Authorization': 'Basic ' + base64_auth_info}  # create the authz header

        try:
            response = requests.get(url=self.url, headers=headers, timeout=60)  # make the request
            response.raise_for_status()  # raise an exception if the request fails
        except requests.exceptions.RequestException as e:
            return e  # return the exception

        with open('/tmp/' + self.get_filename(), 'wb') as f:  # write the response to a file
            f.write(response.text.encode('utf-8'))

        return '/tmp/' + self.get_filename()  # return the file

    @staticmethod
    def get_files():
        """
        Get file
        """
        return db.session.execute(
            db.select(File)
        ).scalars().all()

    @staticmethod
    def get_file_by_id(file_id):
        """
        Get file
        """
        return db.session.execute(
            db.select(File).filter(File.id == file_id)
        ).scalar_one()
