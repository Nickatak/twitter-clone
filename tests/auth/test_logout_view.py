"""Tests for the `logout()` route inside `app.auth.blueprints`.
    This is currently testing with BeautifulSoup4.

    TODO: Implement proper front-end testing with Selenium.
"""
from flask import url_for
import pytest

from app.auth.models import User
from tests.conftest import CleanTestingMixin


class TestRouteBehavior(CleanTestingMixin):
    """Test our logout route's behavior."""

    # TODO: Change this when we remove the `/auth/` prefix from our auth
    # application.
    LOGOUT_URL = '/auth/logout'

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

    def test_route_clears_session(self, app, client, valid_data):
        """Does the route properly clear our `uid` key out of session?"""

        with app.test_request_context():
            new_user = User.create(name=valid_data['name'],
                                   username=valid_data['username'],
                                   email=valid_data['email'],
                                   password=valid_data['password'],
                                   )

            # I see. So you can't send requests with the
            # `session_transaction()` open.  You have to close it first, then
            # send a request, and then re-open it to re-examine the session
            # object.  You also can't use out-of-context things (like our
            # helper functions `do_login`/`do_logout`), so you must set the
            # keys in session manually.
            with client.session_transaction() as session:
                session['uid'] = User.authenticate(
                    valid_data['username'], valid_data['password']).id
                assert 'uid' in session

            # Exmaple of persistence between open-close context managers for
            # `session_transaction()`.
            with client.session_transaction() as session:
                assert 'uid' in session

            resp = client.post(type(self).LOGOUT_URL, follow_redirects=True)
            with client.session_transaction() as session:
                assert resp.status_code == 200
                assert 'uid' not in session

    def test_route_redirects(self, app, client):
        """Does our route redirect us to the unauthorized splash page?"""

        with app.app_context():
            resp = client.post(type(self).LOGOUT_URL, follow_redirects=False)

            assert resp.status_code == 302
            headers = dict(resp.headers)
            assert 'Location' in headers
            assert headers['Location'] == url_for('auth.index')
