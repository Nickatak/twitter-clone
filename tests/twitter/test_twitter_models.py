import pytest

from sqlalchemy.orm.attributes import InstrumentedAttribute

from app import db
from app.auth.models import User
from app.twitter.models import Post, Reply
from tests.conftest import CleanTestingMixin


class TestPostExistence(CleanTestingMixin):
    """Test the existence of our `Post` class."""

    def test_model_exists(self):
        """Does our model exist?"""

        assert Post.__table__ is not None

    def test_model_write(self, app):
        """Can our model be used to write data to the DB?"""

        with app.app_context():
            new_user = User.create(name='test test',
                                   username='Tester',
                                   email='test@test.com',
                                   password='Qweqweqwe123',
                                   )

            new_post = Post(content='Test post content', user=new_user)
            db.session.add(new_post)
            db.session.commit()

            extracted_post = Post.query.first()

            assert extracted_post is not None
            assert extracted_post.content == 'Test post content'
            assert extracted_post.user == new_user


class TestReplyExistence(CleanTestingMixin):
    """Test the existence of our `Reply` class."""

    def test_model_exists(self):
        """Does our model exist?"""

        assert Reply.__table__ is not None

    def test_model_write(self, app):
        """Can our model be used to write data to the DB?"""

        with app.app_context():
            new_user = User.create(name='test test',
                                   username='Tester',
                                   email='test@test.com',
                                   password='Qweqweqwe123',
                                   )

            new_post = Post(content='Test post content', user=new_user)
            reply_post = Post(content='Test reply content', user=new_user)
            new_post.replies.append(reply_post)

            db.session.add(new_post)
            db.session.add(reply_post)
            db.session.commit()

            extracted_post = Post.query.first()

            assert len(Post.query.all()) == 2
            assert extracted_post is not None
            assert extracted_post.content == 'Test post content'
            assert extracted_post.user == new_user
            assert len(extracted_post.replies) == 1

            extracted_reply = extracted_post.replies[0]

            assert extracted_reply.user == new_user
            assert extracted_reply.content == 'Test reply content'
            assert len(extracted_reply.replies_to) == 1
            assert extracted_reply.replies_to[0] == extracted_post


class TestPostFields(CleanTestingMixin):
    """Test the fields on the `Post` class."""

    @pytest.fixture()
    def columns(self):
        """All columns on the `Post` table."""

        return list(Post.__table__.columns)

    @pytest.fixture()
    def column_keys(self, columns):
        """All keys for the columns on the `Post` table."""

        return list(map(lambda c: c.key, columns))

    def test_model_user_fk(self, columns, column_keys):
        """Does our model have our specified `user`/`user_id` fields?"""

        column = columns[column_keys.index('user_id')]

        assert 'user_id' in column_keys
        assert isinstance(column.type, db.Integer)
        assert len(column.foreign_keys) == 1

        assert hasattr(Post, 'user')
        assert isinstance(getattr(Post, 'user'), InstrumentedAttribute)

    def test_model_content(self, columns, column_keys):
        """Does our model have our specified `content` field?"""

        column = columns[column_keys.index('content')]

        assert 'content' in column_keys
        assert isinstance(column.type, db.Text)

    def test_model_replies_fk(self, columns, column_keys):
        """Does our model have our specified `replies` field?"""

        assert hasattr(Post, 'replies')
        assert isinstance(getattr(Post, 'replies'), InstrumentedAttribute)

        assert hasattr(Post, 'replies_to')
        assert isinstance(getattr(Post, 'replies_to'), InstrumentedAttribute)

    def test_model_created_at(self, columns, column_keys):
        """Does our model have our specified `created_at` field?"""

        column = columns[column_keys.index('created_at')]

        assert 'created_at' in column_keys
        assert isinstance(column.type, db.DateTime)

    def test_model_updated_at(self, columns, column_keys):
        """Does our model have our specified `updated_at` field?"""

        column = columns[column_keys.index('updated_at')]

        assert 'updated_at' in column_keys
        assert isinstance(column.type, db.DateTime)


class TestReplyFields(CleanTestingMixin):
    """Test the fields on the `Reply` class."""

    @pytest.fixture()
    def columns(self):
        """All columns on the `Reply` table."""

        return list(Reply.__table__.columns)

    @pytest.fixture()
    def column_keys(self, columns):
        """All keys for the columns on the `Reply` table."""

        return list(map(lambda c: c.key, columns))

    def test_model_target_post_id(self, columns, column_keys):
        """Does our model have our specified `target_post_id` field?"""

        column = columns[column_keys.index('target_post_id')]

        assert 'target_post_id' in column_keys
        assert isinstance(column.type, db.Integer)
        assert len(column.foreign_keys) == 1

    def test_model_reply_post_id(self, columns, column_keys):
        """Does our model have our specified `reply_post_id` field?"""

        column = columns[column_keys.index('reply_post_id')]

        assert 'reply_post_id' in column_keys
        assert isinstance(column.type, db.Integer)
        assert len(column.foreign_keys) == 1
