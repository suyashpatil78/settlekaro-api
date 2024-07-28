import os
from flask import Flask
from flask_smorest import Api
from api.signup import signupBlp

from db import db
from db.models.users import UserModel
from db.models.expenses import ExpenseModel

def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"]="3.0.2"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    api.register_blueprint(signupBlp)

    return app