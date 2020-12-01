"""Tweet model (We're going to call this 'Post')."""

import datetime

from app import db


class Reply(db.Model):
    """M2M Adjoining table from Tweet-Tweet (not a typo).
        This serves to create "reply chains" of tweets.
    """
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    target_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    reply_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Post(db.Model):
    """The Tweet model.
        The reason why I want to call this "Post" is because it's going to be used
        for more than just a "Tweet."  It'll also encompass replies/retweets/etc..
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts', lazy=True)

    # We'll revise this later to include standard tweet character limits.
    content = db.Column(db.Text)
    # Yikes, self-M2M's in SQLAlchemy are kind of difficult and require explicit raw table specification.
    replies = db.relationship('Post',
                              secondary=Reply.__table__,
                              primaryjoin=Reply.__table__.columns.target_post_id == id,
                              secondaryjoin=Reply.__table__.columns.reply_post_id == id,
                              backref=db.backref('replies_to')
                              )

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
