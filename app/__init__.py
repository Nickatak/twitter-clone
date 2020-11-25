from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
# from flask_redis import FlaskRedis


# package-globals
#r = FlaskRedis()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False, template_folder=DevConfig.TEMPLATE_DIR)
    app.config.from_object('config.DevConfig')

    db.init_app(app)
    # r.init_app(app)

    # Register blueprints
    from app import auth

    app.register_blueprint(auth.auth_bp)
    return app



