from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from api.signup.schema import SignupSchema

signupBlp = Blueprint("signup", __name__)

@signupBlp.route('/signup', methods=['POST'])
class Signup(MethodView):
    @signupBlp.arguments(SignupSchema, location='json')
    def post(self, args):
        return jsonify(request.get_json())