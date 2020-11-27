from flask import Blueprint, g, render_template, redirect, session, url_for
from app.auth.models import User

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

    return render_template('twitter/dashboard.html')
