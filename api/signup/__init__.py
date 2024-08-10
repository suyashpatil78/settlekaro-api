from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from api.signup.schema import SignupSchema
import utils.helpers as helpers
from werkzeug.security import generate_password_hash, check_password_hash
from db.models.users import UserModel
from db import db
from flask_jwt_extended import create_access_token, create_refresh_token

signupBlp = Blueprint("signup", __name__)

def assign_user_id() -> str:
    return 'us{0}'.format(helpers.generate_random_string(string_length=10))

def hash_password(password) -> str:
    return generate_password_hash(password)

@signupBlp.route('/api/signup', methods=['POST'])
class Signup(MethodView):
    @signupBlp.arguments(SignupSchema, location='json')
    def post(self, args):
        id = assign_user_id()
        password = hash_password(args['password'])
        username = args['username']

        # if username already exists
        if UserModel.query.filter_by(username=args['username']).first() is not None:
            return jsonify({'message': 'username already exists'}), 400

        # if email already exists
        if UserModel.query.filter_by(email=args['email']).first() is not None:
            return jsonify({'message': 'email already exists'}), 400

        user = UserModel(id=id, username=args['username'], email=args['email'], password=password)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({"acess_token": access_token, "refresh_token": refresh_token}), 201


