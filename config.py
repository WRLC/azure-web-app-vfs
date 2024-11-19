"""
This module contains the configuration settings for the application
"""
import os
from environs import Env

env = Env()


class Config:
    """
    base configuration
    """
    SECRET_KEY = os.getenv("SECRET_APP_KEY")
    SHARED_SECRET = os.getenv("SHARED_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE")
    LOG_FILE = os.getenv("LOG_FILE")
    LOG_DIR = os.getenv("LOG_DIR")
    SITE_URL = os.getenv("SITE_URL")
    SAML_SP = os.getenv("SAML_SP")
    COOKIE_ISSUING_FILE = os.getenv("COOKIE_ISSUING_FILE")
    LOGOUT_SCRIPT = os.getenv("LOGOUT_SCRIPT")
    COOKIE_PREFIX = os.getenv("COOKIE_PREFIX")
    MEMCACHED_SERVER = os.getenv("MEMCACHED_SERVER")
    SERVICE_SLUG = os.getenv("SERVICE_SLUG")
    ADMINS = env.list('ADMINS')

    def __repr__(self):
        return f'<Config {self.SITE_URL}>'

    def __str__(self):
        return f'<Config {self.SITE_URL}>'