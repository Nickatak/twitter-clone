from flask import Blueprint, render_template


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def index():
    """Unauthorized user splash page."""

    return render_template('auth/index.html')