"""Auth routes."""
from flask import Blueprint, redirect, render_template, session, url_for

from app.auth.forms import LoginForm
from app.auth.models import User

# TODO: Remove the url_prefix after we're done making all the routes.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def do_login(user):
    """Helper function to log a user in by setting the primary key (`id`) of a user in a session.
        :user: app.auth.models.User instance, so we can grab the primary key and set it into session.
    """

    session['uid'] = user.id

def do_logout():
    """Helper function to logout a user by clearing all session keys."""

    session.clear()


@auth_bp.route('/')
def index():
    """Unauthorized user splash page."""

    return render_template('auth/index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user is not None:
            do_login(user)
            # TODO: Add a redirect out to the dashboard page (NYI).
            return redirect('/')
        else:
            form.username.errors.append('The username and password you entered did not match our records. Please double-check and try again.')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup')
def signup():
    """User signup page.
        TODO: Build backend handler for user registration.
    """

    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    do_logout()
    return redirect(url_for('auth.index'))

