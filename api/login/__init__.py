from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from api.login.schema import LoginSchema
from werkzeug.security import check_password_hash
from db.models.users import UserModel
from db import db
from flask_jwt_extended import create_access_token

loginBlp = Blueprint("login", __name__)

@loginBlp.route('/login', methods=['POST'])
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

        access_token = create_access_token(identity=user.id)

        return jsonify({"access_token": access_token}), 200


