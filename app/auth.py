from flask import Blueprint, render_template

# TODO: Remove the url_prefix after we're done making all the routes.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def index():
    """Unauthorized user splash page."""

    return render_template('auth/index.html')

@auth_bp.route('/login')
def login():
    """User login page."""

    return render_template('auth/login.html')

@auth_bp.route('/signup')
    """User signup page.
        TODO: Build backend handler for user registration.
    """

    return render_template('auth/signup.html')
