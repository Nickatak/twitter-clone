import pytest

from app import db
from app.auth.models import User
from app.twitter.models import Post, Reply
from tests.conftest import CleanTestingMixin


class TestPostExistence(CleanTestingMixin):
    """Test the existence of our `Post`/`Reply` classes."""

    def test_model_exists(self):
        """Does our model exist?"""

        assert Post.__table__ is not None

    def test_model_write(self, app):
        """Can your model be used to write data to the DB?"""

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
    """Test the existence of our `Post`/`Reply` classes."""

    def test_model_exists(self):
        """Does our model exist?"""

        assert Reply.__table__ is not None

    def test_model_write(self, app):
        """Can your model be used to write data to the DB?"""

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







class TestFields(CleanTestingMixin):
    pass

