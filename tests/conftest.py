"""Pytest configuration file and fixtures."""
from pathlib import Path
import sys

# I have to add the app (package) on Python's PATH before create_app can
# be imported and the tests can be ran.
sys.path.append(str(Path(__file__).parent.parent))


from config import TestConfig
from app import create_app, db

import pytest



flask_app = create_app(TestConfig)


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class CleanTestingMixin(object):
    """Mixin class to provide simple cleanup/teardown operations on a class-base level."""

    def setup_class(self):
        """Drop all existing data and create empty tables prior to running each classes' test cases."""
        with flask_app.app_context():
            db.drop_all()
            db.create_all()
