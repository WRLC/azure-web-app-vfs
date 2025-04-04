"""
This module contains the configuration settings for the application
"""
import os


class Config:
    """
    base configuration
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    SHARED_SECRET = os.getenv("SHARED_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SITE_NAME = os.getenv("SITE_NAME")
    SITE_URL = os.getenv("SITE_URL")
    SAML_SP = os.getenv("SAML_SP")
    COOKIE_ISSUING_FILE = os.getenv("COOKIE_ISSUING_FILE")
    LOGOUT_SCRIPT = os.getenv("LOGOUT_SCRIPT")
    COOKIE_PREFIX = os.getenv("COOKIE_PREFIX")
    MEMCACHED_SERVER = os.getenv("MEMCACHED_SERVER")
    MEMCACHED_PORT = os.getenv("MEMCACHED_PORT")
    SERVICE_SLUG = os.getenv("SERVICE_SLUG")

    def __repr__(self):
        return f'<Config {self.SITE_URL}>'

    def __str__(self):
        return f'<Config {self.SITE_URL}>'
