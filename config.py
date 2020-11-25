from pathlib import Path

class DevConfig(object):
    # It's very unfortunate that you can't enable development-mode without setting Env variables.

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TEMPLATE_DIR = Path(__file__).parent.joinpath('templates')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///blah.sqlite3'