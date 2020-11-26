from flask import Blueprint, render_template

# TODO: Remove the url_prefix after we're done making all the routes.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def index():
    """Unauthorized user splash page."""

    return render_template('auth/index.html')

@auth_bp.route('/login')
def login():
    """Unauthorized user login page."""

    return render_template('auth/login.html')