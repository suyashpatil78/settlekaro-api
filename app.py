import os
from flask import Flask
from flask_smorest import Api
from api.signup import signupBlp
from api.login import loginBlp
from api.users import usersBlp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from db.models.users import UserModel
from db.models.expenses import ExpenseModel

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"]="3.0.2"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    api = Api(app)

    api.register_blueprint(signupBlp)
    api.register_blueprint(loginBlp)
    api.register_blueprint(usersBlp)

    return app