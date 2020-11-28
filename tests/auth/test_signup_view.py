"""Tests for the `signup()` route inside `app.auth.blueprints`.
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


class TestRouteBehavior(CleanTestingMixin):
    """Test our signup route."""

    # TODO: Change this when we remove the `/auth/` prefix from our auth application.
    SIGNUP_URL = '/auth/signup'

    @pytest.fixture
    def form(self, app):
        """Our RegistrationForm instance."""

        with app.app_context():
            return RegistrationForm()

    @pytest.fixture
    def valid_data(self):
        """Reusable valid-data dictionary."""

        return {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
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

    def test_route_inputs(self, client, form):
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

    def test_route_creates_user(self, app, client, valid_data):
        """Does our route create a user given valid data via a POST request?"""

        with app.app_context():
            assert len(User.query.all()) == 0
            resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=True)

            assert resp.status_code == 200
            assert len(User.query.all()) == 1

    def test_route_redirects(self, app, client, valid_data):
        """Does our route return a redirect to our dashboard route after being given valid data via a POST request?"""

        resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=False)

        with app.app_context():
            assert resp.status_code == 302
            headers = dict(resp.headers)
            assert 'Location' in headers
            assert headers['Location'] == url_for('twitter.dashboard')

    def test_after_reg_signin(self, app, client, valid_data):
        """Does our route sign us in after being given valid data via a POST request?"""

        resp = client.post(type(self).SIGNUP_URL, data=valid_data, follow_redirects=True)

        with app.app_context():
            user = User.query.first()
            with client.session_transaction() as session:
                assert 'uid' in session
                assert session['uid'] == user.id


class TestFormBehavior(CleanTestingMixin):

    # TODO: Change this when we remove the `/auth/` prefix from our auth application.
    SIGNUP_URL = '/auth/signup'

    @pytest.fixture
    def form(self, app):
        """Our RegistrationForm instance."""

        with app.app_context():
            return RegistrationForm()

    @pytest.fixture
    def valid_data(self):
        """Reusable valid-data dictionary."""

        return {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
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

    def test_fail_omit_name(self, client, form):
        """Does our route fail if we omit the `name` on the field?"""

        invalid_data = {
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.name.validators[0].message

    def test_fail_omit_username(self, client, form):
        """Does our route fail if we omit the `username` on the field?"""

        invalid_data = {
            'name' : 'test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.username.validators[0].message

    def test_fail_omit_email(self, client, form):
        """Does our route fail if we omit the `email` on the field?"""

        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'password' : 'Qweqweqwe123',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.email.validators[0].message

    def test_fail_omit_password(self, client, form):
        """Does our route fail if we omit the `password` on the field?"""

        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'month' : 1, #January 1st, 2000.
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.password.validators[0].message

    def test_fail_omit_month(self, client, form):
        """Does our route fail if we omit the `month` on the field?"""

        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'day' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.month.validators[0].message

    def test_fail_omit_day(self, client, form):
        """Does our route fail if we omit the `day` on the field?"""

        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'year' : 2000, 
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.day.validators[0].message

    def test_fail_omit_year(self, client, form):
        """Does our route fail if we omit the `year` on the field?"""

        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        # The first element in our validators will always be `DataRequired()`
        assert errors[0].decode_contents() == form.year.validators[0].message

    def test_fail_invalid_name(self, client):
        """Does our route fail if we send invalid data for the `name` field?
            1. Too long (> 50 chars).
        """

        # 1. Too long (> 50 chars).
        invalid_data = {
            'name' : 'a' * 51,
            'username' : 'tester',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Name cannot be longer than 50 characters.'

    def test_fail_invalid_username(self, client):
        """Does our route fail if we send invalid data for the `username` field?
            1. Too long (> 15 chars).
            2. @
            3. #
            4. (spaces)
            5. *
            6. !
            7. ?
            8. '
            9. "
            10. -
            11. /
            12. \\
            13. =
            14. +
            15. %
            16. $
            17. (
            18. <
            19. .
        
        """

        # Too long (> 15 chars).
        invalid_data = {
            'name' : 'test test',
            'username' : 'a' * 16,
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Username cannot be longer than 15 characters.'

        # 2. Special Char (@).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test@test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 3. Special Char (#).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test#test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 4. Spaces ( ).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 5. Asterisks (*).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test*test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 6. Exclamation marks (!).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test!test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 7. Question marks (?).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test?test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 8. Quotation marks (').
        invalid_data = {
            'name' : 'test test',
            'username' : "test'test",
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 9. Double-Quotation marks (").
        invalid_data = {
            'name' : 'test test',
            'username' : 'test"test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 10. Dashes (-).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test-test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 11. Slashes (/).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test/test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 12. Backslashes (\).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test\\test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 13. Equals (=).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test=test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 14. Plus (+).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test+test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # Carat (^).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test^test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 15. Percentage (%).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test%test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 16. Dollar Sign ($).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test%test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 17. Parenthesis-Open (().
        invalid_data = {
            'name' : 'test test',
            'username' : 'test(test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 18. Less-than (<).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test<test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

        # 19. Period (.).
        invalid_data = {
            'name' : 'test test',
            'username' : 'test.test',
            'email' : 'test@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Must be letters (uppercase or lowercase), digits, and underscores only.'

    def test_fail_invalid_email(self, client):
        """Does our route fail if we send invalid data for the `email` field?
            1. Too long (> 100 chars).
            2. Missing @ sign.
            3. Missing domain.
            4. Missing front.
        """

        # 1. Too long (> 100 chars).
        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'a' * 101,
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 2
        assert errors[0].decode_contents() == 'Email cannot be longer than 100 characters.'
        assert errors[1].decode_contents() == 'Email must be valid.'

        # 2. Missing @ sign.
        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'testest.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Email must be valid.'

        # 3. Missing domain.
        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : 'test@test',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Email must be valid.'

        # 2. Missing front.
        invalid_data = {
            'name' : 'test test',
            'username' : 'tester',
            'email' : '@test.com',
            'password' : 'Qweqweqwe123',
            'month' : 1,
            'day' : 1,
            'year' : 2020,
        }

        resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
        html = BeautifulSoup(resp.data, 'html.parser')

        errors = html.find_all('p', {'class' : 'twitter-text error'})

        assert len(errors) == 1
        assert errors[0].decode_contents() == 'Email must be valid.'

    def test_fail_username_unique(self, app, client, valid_data):
        """Does our route fail if we send already-existing data for the `username` field?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
            )

            # Same username, different email
            invalid_data = {
                'name' : 'test test',
                'username' : 'tester',
                'email' : 'asdf@test.com',
                'password' : 'Qweqweqwe123',
                'month' : 1, #January 1st, 2000.
                'day' : 1,
                'year' : 2000, 
            }

            resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
            html = BeautifulSoup(resp.data, 'html.parser')

            errors = html.find_all('p', {'class' : 'twitter-text error'})

            assert len(errors) == 1
            assert errors[0].decode_contents() == 'Username must be unique.'

    def test_fail_email_unique(self, app, client, valid_data):
        """Does our route fail if we send already-existing data for the `email` field?"""

        with app.app_context():
            User.create(name=valid_data['name'],
                        username=valid_data['username'],
                        email=valid_data['email'],
                        password=valid_data['password'],
            )

            # Same email, different username
            invalid_data = {
                'name' : 'test test',
                'username' : 'asdf',
                'email' : 'test@test.com',
                'password' : 'Qweqweqwe123',
                'month' : 1, #January 1st, 2000.
                'day' : 1,
                'year' : 2000, 
            }

            resp = client.post(type(self).SIGNUP_URL, data=invalid_data, follow_redirects=True)
            html = BeautifulSoup(resp.data, 'html.parser')

            errors = html.find_all('p', {'class' : 'twitter-text error'})

            assert len(errors) == 1
            assert errors[0].decode_contents() == 'Email must be unique.'
