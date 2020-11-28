import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class DevConfig(object):
    # It's very unfortunate that you can't enable development-mode without setting Env variables.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
            BASE_DIR.joinpath('blah.sqlite3')
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_DIR = BASE_DIR.joinpath('static')
    TEMPLATE_DIR = BASE_DIR.joinpath('templates')
    SECRET_KEY = os.urandom(24)


class TestConfig(DevConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
            BASE_DIR.joinpath('testing.sqlite3')
        )
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain:5000'
