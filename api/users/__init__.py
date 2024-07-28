from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from api.users.schema import UsersSchema
from werkzeug.security import check_password_hash
from db.models.users import UserModel
from db import db
from flask_jwt_extended import create_access_token, jwt_required

usersBlp = Blueprint("users", __name__)

@usersBlp.route('/users', methods=['GET'])
class Users(MethodView):
    @jwt_required()
    @usersBlp.response(200, UsersSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users