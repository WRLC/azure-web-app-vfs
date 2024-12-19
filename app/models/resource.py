import os
from typing import TYPE_CHECKING
from base64 import b64encode
import requests
import sqlalchemy.engine.result
from flask import Response
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
    app_description: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f'<Resource: {self.app_name}>'

    @staticmethod
    def get_all() -> list:
        """
        Get all resources

        :return: all resources
        """
        return db.session.execute(db.select(Resource)).scalars().all()

    @staticmethod
    def get_by_id(resource_id: int) -> sqlalchemy.engine.result.Result | None:
        """
        Get a resource by ID

        :param resource_id: resource ID
        :return: the resource
        """
        return db.session.execute(db.select(Resource).filter_by(id=resource_id)).scalar_one_or_none()

    def get_files_by_path(self, **kwargs) -> Exception | list | None:
        """
        Get files by path

        :param kwargs: keyword arguments
        :return: files
        """
        fullurl = self.get_url(kwargs)  # get the URL
        base64_auth_info = self.encode_auth_info()  # encode the username and password
        headers = self.set_headers(base64_auth_info)  # create the authz header

        return self.request_url(fullurl, headers)  # make the request and return the files

    def download_file(self, **kwargs) -> str | Exception:
        """
        Download file
        """
        fullurl = self.get_url(kwargs)  # get the URL
        base64_auth_info = self.encode_auth_info()  # encode the username and password
        headers = self.set_headers(base64_auth_info)  # create the authz header
        response = self.request_url(fullurl, headers)  # make the request

        return self.write_file(fullurl, response)  # write the file and return the path

    def get_url(self, kwargs: dict) -> str:
        """
        Get the URL
        """
        return f'{self.url}{kwargs.get("path", "")}'  # return the URL

    def encode_auth_info(self) -> str:
        """
        Encode the username and password
        """
        return b64encode(  # encode the username and password
            (self.username + ':' + self.password).encode('ascii')
        ).decode('ascii')

    @staticmethod
    def set_headers(auth: str) -> dict:
        """
        Set the headers
        """
        return {'Authorization': 'Basic ' + auth}  # return the headers

    @staticmethod
    def request_url(url: str, headers: dict) -> Response | Exception:
        """
        Request a url
        """
        try:
            response = requests.get(url=f'{url}', headers=headers, timeout=60)  # make the request
            response.raise_for_status()  # raise an exception if the status is not 200
        except requests.exceptions.RequestException as error:  # handle the exception
            return error  # return the error

        return response  # return the response

    def write_file(self, url: str, response: requests.Response) -> str | Exception:
        """
        Write a file
        """
        if isinstance(response, Exception):  # if the response is an exception,
            return response  # return the exception
        try:
            with open('/tmp/' + self.get_filename(url), 'wb') as f:  # write the data to the file
                f.write(response.text.encode('utf-8'))
        except Exception as error:  # handle the exception
            return error  # return the error

        return f'/tmp/{self.get_filename(url)}'  # return the path to the file

    @staticmethod
    def get_filename(url: str) -> str:
        """
        Get the filename from a url
        """
        return os.path.basename(url)  # return the filename
