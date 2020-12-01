from flask import Blueprint, g, render_template, redirect, request, session, url_for

from app import db
from app.twitter.models import Post

twitter_bp = Blueprint('twitter', __name__)


@twitter_bp.before_request
def assign_uid():
    if 'uid' in session:
        g.uid = session['uid']
    else:
        g.uid = None


@twitter_bp.route('/home')
def dashboard():
    """Twitter Clone Dashboard.
        TODO: Implement this.
    """

    # Simple unauthorized redirect.
    if g.uid is None:
        return redirect(url_for('auth.login'))

    all_posts = Post.query.all()

    return render_template('twitter/dashboard.html', all_posts=all_posts)


@twitter_bp.route('/posts/create', methods=['POST'])
def create_post():
    """Create a new POST
        This is currently here just for minimally-working testing.

        TODO: Implement this.
    """

    # Simple unauthorized redirect.
    if g.uid is None:
        return redirect(url_for('auth.login'))

    new_post = Post(
        user_id=g.uid,
        content=request.form['content'],
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('twitter.dashboard'))
