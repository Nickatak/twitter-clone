from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis


# package-globals
app = Flask(__name__)
#r = FlaskRedis()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    db.init_app(app)
    # r.init_app(app)
    with app.app_context():
        from app import auth

        app.register_blueprint(auth.auth_bp)

    return app



