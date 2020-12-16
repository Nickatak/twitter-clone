from flask import Blueprint, g, render_template, redirect, request, session, url_for

from app import db
from app.auth.models import User
from app.twitter.models import Post

twitter_bp = Blueprint('twitter', __name__)


@twitter_bp.before_request
def assign_user():
    """I might have to revise this later,
        but since the user information is required on the navbar rendering,
        I don't think another query is avoidalbe right now.
     """

    if 'uid' in session:
        g.user = User.query.get(session['uid'])
    else:
        g.user = None


@twitter_bp.route('/home')
def dashboard():
    """Twitter Clone Dashboard.

        TODO: Implement this. Currently being worked on by: Ethan.
    """

    # Simple unauthorized redirect.
    if g.user is None:
        return redirect(url_for('auth.login'))

    all_posts = Post.query.all()

    return render_template('twitter/dashboard.html', all_posts=all_posts)


@twitter_bp.route('/posts/create', methods=['POST'])
def create_post():
    """Create a new POST.
        This is currently here just for minimally-working testing.

        TODO: Implement this.
    """

    # Simple unauthorized redirect.
    if g.user is None:
        return redirect(url_for('auth.login'))

    new_post = Post(
        user_id=g.user.id,
        content=request.form['content'],
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('twitter.dashboard'))


@twitter_bp.route('/<username>')
def view_user(username):
    """View a user's profile.
        This route may be viewed by an unauthorized user.

        TODO: Implement this. Currently being worked on by: Nick.
    """

    user = User.get_by_username_or_404(username)

    all_posts = Post.query.all()

    return render_template('twitter/profile.html', user=user, all_posts=all_posts)
