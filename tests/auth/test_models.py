"""Tests for app.auth.models.User class."""
import pytest

from app import db
from app.auth.models import User

class TestExistence:
    def test_model_exists(self):
        """Does our model exist?"""

        assert User.__table__ is not None

    def test_model_write(self, app):
        """Can your model be used to write data to the DB?"""

        with app.app_context():
            new_user = User(
                username='Test',
                phone='1231231234',
                email='test@test.com',
                password='',
            )

            db.session.add(new_user)
            db.session.commit()

            extracted_user = User.query.first()

            assert extracted_user is not None
            assert extracted_user.username == 'Test'
            assert extracted_user.phone == '1231231234'
            assert extracted_user.email == 'test@test.com'

class TestFields:

    @pytest.fixture()
    def columns(self):
        return list(User.__table__.columns)

    @pytest.fixture()
    def column_keys(self, columns):
        return list(map(lambda c: c.key, columns))

    def test_model_id(self, columns, column_keys):
        """Does our model have our specified `id` field?"""

        column = columns[column_keys.index('id')]

        assert 'id' in column_keys
        assert isinstance(column.type, db.Integer)
        assert column.primary_key
        assert column.autoincrement

    def test_model_username(self, columns, column_keys):
        """Does our model have our specified `username` field?"""

        column = columns[column_keys.index('username')]

        assert 'username' in column_keys
        assert isinstance(column.type, db.String)
        assert column.type.length == 15
        assert column.unique

    def test_model_phone(self, columns, column_keys):
        """Does our model have our specified `phone` field?"""

        column = columns[column_keys.index('phone')]

        assert 'phone' in column_keys
        assert isinstance(column.type, db.String)
        assert column.type.length == 30
        assert column.unique

    def test_model_email(self, columns, column_keys):
        """Does our model have our specified `email` field?"""

        column = columns[column_keys.index('email')]

        assert 'email' in column_keys
        assert isinstance(column.type, db.String)
        assert column.type.length == 100
        assert column.unique

    def test_model_email(self, columns, column_keys):
        """Does our model have our specified `password` field?"""

        column = columns[column_keys.index('password')]

        assert 'password' in column_keys
        assert isinstance(column.type, db.String)
        assert column.type.length == 256