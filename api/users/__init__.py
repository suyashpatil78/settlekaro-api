from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from api.users.schema import UsersSchema
from werkzeug.security import check_password_hash
from db.models.users import UserModel
from db import db
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy import func

usersBlp = Blueprint("users", __name__)

@usersBlp.route('/users', methods=['GET'])
class Users(MethodView):
    @jwt_required()
    @usersBlp.response(200, UsersSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users
    

@usersBlp.route('/users/<string:id>', methods=['GET'])
class User(MethodView):
    @jwt_required()
    @usersBlp.response(200, UsersSchema)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        return user
    

@usersBlp.route('/users/search/<string:username>', methods=['GET'])
class SearchUser(MethodView):
    @jwt_required()
    @usersBlp.response(200, UsersSchema(many=True))
    def get(self, username):
        username = username.lower()
        users = UserModel.query.filter(func.lower(UserModel.username).like(f'%{username}%')).all()
        return users