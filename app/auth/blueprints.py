"""Auth routes."""
from flask import Blueprint, render_template, session

# TODO: Remove the url_prefix after we're done making all the routes.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login(user):
    """Helper function to log a user in by setting the primary key (`id`) of a user in a session.
        :user: app.auth.models.User instance, so we can grab the primary key and set it into session.
    """

    session['uid'] = user.id

def logout():
    """Helper function to logout a user by clearing all session keys."""

    session.clear()


@auth_bp.route('/')
def index():
    """Unauthorized user splash page."""

    return render_template('auth/index.html')

@auth_bp.route('/login')
def login():
    """User login page."""

    return render_template('auth/login.html')

@auth_bp.route('/signup')
def signup():
    """User signup page.
        TODO: Build backend handler for user registration.
    """

    return render_template('auth/signup.html')
