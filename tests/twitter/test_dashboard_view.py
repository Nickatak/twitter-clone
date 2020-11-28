"""Tests for the `dashboard()` route inside `app.twitter.blueprints`."""
from flask import url_for
from tests.conftest import CleanTestingMixin


class TestRouteBehavior(CleanTestingMixin):
    DASHBOARD_URL = '/home'

    def test_unauth_redirect(self, app, client):
        resp = client.get(type(self).DASHBOARD_URL, follow_redirects=False)

        with app.app_context():
            assert resp.status_code == 302
            headers = dict(resp.headers)
            assert 'Location' in headers
            assert headers['Location'] == url_for('auth.login')
