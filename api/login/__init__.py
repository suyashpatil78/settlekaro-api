from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from api.login.schema import LoginSchema
from werkzeug.security import check_password_hash
from db.models.users import UserModel
from db import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token

loginBlp = Blueprint("login", __name__)

@loginBlp.route('/api/login', methods=['POST'])
class Login(MethodView):
    @loginBlp.arguments(LoginSchema, location='json')
    def post(self, args):
        email = args['email']
        password = args['password']

        user = UserModel.query.filter_by(email=email).first()

        if user is None:
            return jsonify({'message': 'user does not exist'}), 400

        if not check_password_hash(user.password, password):
            return jsonify({'message': 'invalid password'}), 400

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify({"access_token": access_token, "refresh_token": refresh_token, "email": email, "id": user.id, "username": user.username}), 200

@loginBlp.route('/api/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
class Refresh(MethodView):
    def post(self, args):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = args['refresh_token']

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200