"""Tests for `app.auth.models.User` class."""
import pytest

from app import db, bcrypt
from app.auth.models import User
from tests.conftest import CleanTestingMixin


class TestExistence(CleanTestingMixin):
    """Test the existence of our `User` class."""    

    def test_model_exists(self):
        """Does our model exist?"""

        assert User.__table__ is not None

    def test_model_write(self, app):
        """Can your model be used to write data to the DB?"""

        with app.app_context():
            new_user = User(
                username='Test',
                email='test@test.com',
                password='',
            )

            db.session.add(new_user)
            db.session.commit()

            extracted_user = User.query.first()

            assert extracted_user is not None
            assert extracted_user.username == 'Test'
            assert extracted_user.email == 'test@test.com'

class TestFields(CleanTestingMixin):
    """Test the fields on the `User` class."""

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

    """
    def test_model_phone(self, columns, column_keys):
        \"\"\"Does our model have our specified `phone` field?\"\"\"

        column = columns[column_keys.index('phone')]

        assert 'phone' in column_keys
        assert isinstance(column.type, db.String)
        assert column.type.length == 30
        assert column.unique
    """

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

class TestHelpers(CleanTestingMixin):
    """Test the helper methods for the `User` class."""

    def test_model_create(self, app):
        """Does our static method `User.create()` store information in the DB?"""

        with app.app_context():
            new_user = User.create(name='tester',
                                username='testing',
                                email='testing@testing.com',
                                password='Qweqweqwe123'
            )
            user = User.query.first()

            assert user is not None
            assert user.name == 'tester'
            assert user.username == 'testing'
            assert user.email == 'testing@testing.com'
            assert user.password != 'Qweqweqwe123'

    def test_model_pwd_hash(self, app):
        """Does our static method `User.create()` use bcrypt to hash the password?"""

        with app.app_context():
            user = User.query.first()
            assert user is not None
            # This is the current bcrypt algorithm signature (Dec. 2020)
            assert user.password[0:4] == '$2b$'

    def test_model_authenticate(self, app):
        """Does our static method `User.authenticate()` retrieve an existing user given a correct username/PW combination?"""

        with app.app_context():
            user = User.query.first()

            att_user = User.authenticate('testing', 'Qweqweqwe123')

            assert att_user is not None
            assert user.id == att_user.id
            assert user.username == att_user.username
            assert user.password == att_user.password

    def test_model_unauth(self, app):
        """Does our static method `User.authenticate()` fail properly (return a NoneType) when given an incorrect username/PW combination?"""

        with app.app_context():
            #Non existent username:
            att_user = User.authenticate('asdf', 'asdf')
            assert att_user is None

            #Existing username but bad password:
            att_user = User.authenticate('testing', 'asdf')
            assert att_user is None

            #Correct password but non existing username:
            att_user = User.authenticate('asdf', 'Qweqweqwe123')
            assert att_user is None
