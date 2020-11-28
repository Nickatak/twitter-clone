"""Tests for the routes inside `app.auth.blueprints`.
    This is currently testing with BeautifulSoup4.  Later on we'll use a proper web-driver like Selenium to do FE-testing.

    TODO: Implement proper front-end testing.
"""
from bs4 import BeautifulSoup
from flask import url_for
import pytest

from app import db, bcrypt
from app.auth.models import User
from app.auth.forms import RegistrationForm
from tests.conftest import CleanTestingMixin


class TestSignup(CleanTestingMixin):
    """Test our signup route"""

    # TODO: Change this when we remove the `/auth/` prefix from our auth application.
    SIGNUP_URL = '/auth/signup'

    @pytest.fixture
    def form(self, app):
        """Our RegistrationForm instance."""

        with app.app_context():
            return RegistrationForm()

    @pytest.fixture(autouse=True)
    def run_after_every_test(self, app):
        """Delete all the users in the DB after every test.
            Special Note: Does NOT DROP the tables.
        """
        yield

        with app.app_context():
            User.query.delete()
            db.session.commit()


    def test_route_GET(self, client):
        """Does our route handle GET requests?"""

        resp = client.get(type(self).SIGNUP_URL)

        assert resp.status_code == 200
        assert resp.data

    def test_route_POST(self, client):
        """Does our route handle POST requests?"""
        resp = client.post(type(self).SIGNUP_URL)

        assert resp.status_code == 200

    def test_route_form(self, client):
        """Does our route have a form on it when we send a GET?"""

        resp = client.get(type(self).SIGNUP_URL)
        html = BeautifulSoup(resp.data, 'html.parser')

        assert html.find('form') is not None

    def test_route_inputs(self, app, client, form):
        """Does our route return a page that has the required inputs on it when we send a GET?"""

        resp = client.get(type(self).SIGNUP_URL)
        html = BeautifulSoup(resp.data, 'html.parser')
        html_form = html.find('form')

        # Is there a "Name" input with a proper label of "Name"?
        ele = html_form.find('input', {'id' : "name"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find('label').decode_contents() == form.name.label.text

        # Is there a "Username" input with a proper label of "Username"?
        ele = html_form.find('input', {'id' : "username"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find('label').decode_contents() == form.username.label.text

        # Is there a "Email" input with a proper label of "Email"?
        ele = html_form.find('input', {'id' : "email"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find('label').decode_contents() == form.email.label.text

        # Is there a "Password" input with a proper label of "Password"?
        ele = html_form.find('input', {'id' : "password"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find('label').decode_contents() == form.password.label.text

        # Is there a "Month" select-tag with a proper label of "Month" and does it have children (option tags)?
        ele = html_form.find('select', {'id' : "month"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert len(tuple(ele.children))
        assert ele.parent.find('label').decode_contents() == form.month.label.text

        # Is there a "Day" select-tag with a proper label of "Day" and does it have children (option tags)?
        ele = html_form.find('select', {'id' : "day"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert len(tuple(ele.children))
        assert ele.parent.find('label').decode_contents() == form.day.label.text

        # Is there a "year" select-tag with a proper label of "year" and does it have children (option tags)?
        ele = html_form.find('select', {'id' : "year"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert len(tuple(ele.children))
        assert ele.parent.find('label').decode_contents() == form.year.label.text

    def test_route_creates_user(self, app, client):
        """Does our route create a user given valid data via a POST request?"""

        valid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        with app.app_context():
            assert len(User.query.all()) == 0
            resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=True)

            assert resp.status_code == 200
            assert len(User.query.all()) == 1

    def test_route_redirects(self, app, client):
        """Does our route return a redirect to our dashboard route after being given valid data via a POST request?"""

        valid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=False)

        with app.app_context():
            assert resp.status_code == 302
            headers = dict(resp.headers)
            assert 'Location' in headers
            assert headers['Location'] == url_for('twitter.dashboard')

    def test_after_reg_signin(self, app, client):
        """Does our route sign us in after being given valid data via a POST request?"""

        valid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=True)

        with app.app_context():
            user = User.query.first()
            with client.session_transaction() as session:
                assert 'uid' in session
                assert session['uid'] == user.id
