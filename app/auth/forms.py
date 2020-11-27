from flask_wtf import FlaskForm
from wtforms import StringField
# wtforms.validators import We'll see if we need any right now.

class LoginForm(FlaskForm):
    username = StringField('Phone, email, or username')
    password = StringField()