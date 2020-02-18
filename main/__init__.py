from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from .config import app_environment

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(env_config):
    app = Flask(__name__)
    app.config.from_object(app_environment[env_config])
    db.init_app(app)
    bcrypt.init_app(app)
    app.config["JWT_SECRET_KEY"] = "githinvgeorge"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
    # app.config["JWT_HEADER_NAME"] = ("Authorization", "X-API-KEY")
    jwt = JWTManager(app)
    return app

