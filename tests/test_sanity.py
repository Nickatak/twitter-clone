"""Sanity tests to make sure your tests are running.  Contains 4 tests."""
from flask import Flask
from flask.testing import FlaskClient


def test_sanity_truthy():
    assert True


def test_sanity_falsey():
    assert False == False


def test_app_fixture(app):
    assert isinstance(app, Flask)


def test_client_fixture(client):
    assert isinstance(client, FlaskClient)
