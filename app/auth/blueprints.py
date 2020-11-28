"""Auth routes."""
from flask import Blueprint, redirect, render_template, session, url_for

from app.auth.forms import LoginForm, RegistrationForm
from app.auth.models import User

# TODO: Remove the url_prefix after we're done making all the routes.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def do_login(user):
    """Helper function to log a user in by setting the primary key (`id`) of a user in a session.  Having this separated will be useful if we ever want to send alerts on login or something like that.
        :user: app.auth.models.User instance, so we can grab the primary key and set it into session.
    """

    session['uid'] = user.id


def do_logout():
    """Helper function to logout a user by clearing all session keys.  Having this separated will be useful if we ever want to send alerts on login or something like that."""

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
            return redirect(url_for('twitter.dashboard'))
        else:
            form.username.errors.append(
                'The username and password you entered did not match our records. Please double-check and try again.')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page."""

    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User.create(form.name.data,
                               form.username.data,
                               form.email.data,
                               form.password.data,
                               )
        do_login(new_user)

        return redirect(url_for('twitter.dashboard'))

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout route."""

    do_logout()
    print(session)
    print('-' * 50)
    return redirect(url_for('auth.index'))
