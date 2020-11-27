"""Pytest configuration file and fixtures."""

from pathlib import Path
import pytest
import sys

# I have to add the app (package) on Python's PATH before create_app can be imported and the tests can be ran.
sys.path.append(str(Path(__file__).parent.parent))

from app import create_app
flask_app = create_app()

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
