"""Tests for the `login()` route inside `app.auth.blueprints`.
    This is currently testing with BeautifulSoup4.  Later on we'll use a proper web-driver like Selenium to do FE-testing.

    TODO: Implement proper front-end testing.
"""
from bs4 import BeautifulSoup
from flask import url_for
import pytest

from app import db
from app.auth.models import User
from app.auth.forms import LoginForm
from tests.conftest import CleanTestingMixin


class TestRouteBehavior(CleanTestingMixin):
    """Test our login route's behavior."""

    # TODO: Change this when we remove the `/auth/` prefix from our auth
    # application.
    LOGIN_URL = '/auth/login'

    @pytest.fixture
    def form(self, app):
        """Our LoginForm instance."""

        with app.app_context():
            return LoginForm()

    @pytest.fixture
    def valid_data(self):
        """Reusable valid-data dictionary."""

        return {
            'name': 'test test',
            'username': 'tester',
            'email': 'test@test.com',
            'password': 'Qweqweqwe123',
            'month': 1,  # January 1st, 2000.
            'day': 1,
            'year': 2000,
        }

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

        resp = client.get(type(self).LOGIN_URL)

        assert resp.status_code == 200
        assert resp.data

    def test_route_POST(self, client):
        """Does our route handle POST requests?"""

        resp = client.post(type(self).LOGIN_URL)

        assert resp.status_code == 200

    def test_route_form(self, client):
        """Does our route have a form on it when we send a GET?"""

        resp = client.get(type(self).LOGIN_URL)
        html = BeautifulSoup(resp.data, 'html.parser')

    def test_route_inputs(self, app, client, form):
        """Does our route return a page that has the required inputs on it when we send a GET?"""

        resp = client.get(type(self).LOGIN_URL)
        html = BeautifulSoup(resp.data, 'html.parser')
        html_form = html.find('form')

        # Is there a "Username" input with a proper label of "Username"?
        ele = html_form.find('input', {'id': "username"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find(
            'label').decode_contents() == form.username.label.text

        # Is there a "Password" input with a proper label of "Password"?
        ele = html_form.find('input', {'id': "password"})
        assert ele is not None
        assert ele.parent.find('label') is not None
        assert ele.parent.find(
            'label').decode_contents() == form.password.label.text

    def test_route_logs_in(self, app, client, valid_data):
        """Does our route log us in given valid data via a POST request?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
                        )

            resp = client.post(type(self).LOGIN_URL,
                               data=valid_data, follow_redirects=True)
            user = User.query.first()

            with client.session_transaction() as session:
                assert 'uid' in session
                assert session['uid'] == user.id

    def test_route_redirects(self, app, client, valid_data):
        """Does our route return a redirect to our dashboard route after being given valid data via a POST request?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
                        )

            resp = client.post(type(self).LOGIN_URL,
                               data=valid_data, follow_redirects=False)

            assert resp.status_code == 302
            headers = dict(resp.headers)
            assert 'Location' in headers
            assert headers['Location'] == url_for('twitter.dashboard')


class TestFormValidationBehavior(CleanTestingMixin):
    """Test our LoginForm's behavior."""

    # TODO: Change this when we remove the `/auth/` prefix from our auth
    # application.
    LOGIN_URL = '/auth/login'

    @pytest.fixture
    def form(self, app):
        """Our LoginForm instance."""

        with app.app_context():
            return LoginForm()

    @pytest.fixture
    def valid_data(self):
        """Reusable valid-data dictionary."""

        return {
            'name': 'test test',
            'username': 'tester',
            'email': 'test@test.com',
            'password': 'Qweqweqwe123',
            'month': 1,  # January 1st, 2000.
            'day': 1,
            'year': 2000,
        }

    @pytest.fixture(autouse=True)
    def run_after_every_test(self, app):
        """Delete all the users in the DB after every test.
            Special Note: Does NOT DROP the tables.
        """

        yield

        with app.app_context():
            User.query.delete()
            db.session.commit()

    def test_fail_omit_username(self, app, form, client, valid_data):
        """Does our route fail if we omit the `username` on the form?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
                        )

            invalid_data = {
                'password': 'Qweqweqwe123',
            }

        resp = client.post(type(self).LOGIN_URL,
                           data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class': 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents(
        ) == form.username.validators[0].message

    def test_fail_omit_password(self, app, form, client, valid_data):
        """Does our route fail if we omit the `password` on the form?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
                        )

            invalid_data = {
                'username': 'tester',
            }

        resp = client.post(type(self).LOGIN_URL,
                           data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class': 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents(
        ) == form.password.validators[0].message

    def test_fail_invalid_combination(self, app, client, valid_data):
        """Does our route fail if we send invalid data?"""
        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
                        )

            # Correct username, but incorrect password.
            invalid_data = {
                'username': 'tester',
                'password': 'notmypassword',
            }

            resp = client.post(type(self).LOGIN_URL,
                               data=invalid_data, follow_redirects=True)
            html = BeautifulSoup(resp.data, 'html.parser')

            errors = html.find_all('p', {'class': 'twitter-text error'})

            assert len(errors) == 1
            # The first element in our validators will always be
            # `DataRequired()`
            assert errors[0].decode_contents(
            ) == 'The username and password you entered did not match our records. Please double-check and try again.'

            # Correct password but incorrect username.
            invalid_data = {
                'username': 'asdf',
                'password': 'Qweqweqwe123',
            }

            resp = client.post(type(self).LOGIN_URL,
                               data=invalid_data, follow_redirects=True)
            html = BeautifulSoup(resp.data, 'html.parser')

            errors = html.find_all('p', {'class': 'twitter-text error'})

            assert len(errors) == 1
            # The first element in our validators will always be
            # `DataRequired()`
            assert errors[0].decode_contents(
            ) == 'The username and password you entered did not match our records. Please double-check and try again.'
