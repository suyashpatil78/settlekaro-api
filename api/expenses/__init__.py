from flask.views import MethodView
from flask_smorest import Blueprint
from db.models.expenses import ExpenseModel
from db.models.users import UserModel
from api.expenses.schema import ExpensesSchema
from db import db
from flask_jwt_extended import jwt_required
from utils import helpers
from datetime import datetime

expensesBlp = Blueprint("expenses", __name__)

def assign_expense_id() -> str:
    return 'ex{0}'.format(helpers.generate_random_string(string_length=10))

@expensesBlp.route("/expenses", methods=["GET", "POST"])
class Expenses(MethodView):
    @jwt_required()
    @expensesBlp.response(200, ExpensesSchema(many=True))
    def get(self):
        expenses = ExpenseModel.query.all()
        return expenses
    
    @jwt_required()
    @expensesBlp.response(201, ExpensesSchema)
    @expensesBlp.arguments(ExpensesSchema, location='json')
    def post(self, args):
        id = assign_expense_id()
        created_by = args['created_by']
        amount = args['amount']
        expense_details = args['expense_details']
        
        date = datetime.strptime(args['date'], '%Y-%m-%d')
        
        expense = ExpenseModel(id=id, created_by=created_by, amount=amount, expense_details=expense_details, date=date)
        
        db.session.add(expense)

        # add the expense to all the user's expenses
        for expense_detail in expense_details:
            user = UserModel.query.filter_by(id=expense_detail['user_id']).first()
            expense_id = expense.id
            user_expenses = user.expenses if user.expenses else []
            user_expenses.append(expense_id)
            user.expenses = user_expenses

        db.session.commit()
        
        return expense
    
@expensesBlp.route("/expenses/<string:id>", methods=["GET", "PUT", "DELETE"])
class Expense(MethodView):
    @jwt_required()
    @expensesBlp.response(200, ExpensesSchema)
    def get(self, id):
        expense = ExpenseModel.query.filter_by(id=id).first()
        return expense
    
    @jwt_required()
    @expensesBlp.response(200, ExpensesSchema)
    @expensesBlp.arguments(ExpensesSchema, location='json')
    def put(self, args, id):
        expense = ExpenseModel.query.filter_by(id=id).first()
        
        expense.created_by = args['created_by']
        expense.amount = args['amount']
        expense.expense_details = args['expense_details']
        
        db.session.commit()
        
        return expense
    
    @jwt_required()
    @expensesBlp.response(204)
    def delete(self, id):
        expense = ExpenseModel.query.filter_by(id=id).first()
        db.session.delete(expense)
        db.session.commit()
        return None


@expensesBlp.route("/expenses/user", methods=["GET"])
class UserExpenses(MethodView):
    @jwt_required()
    @expensesBlp.response(200, ExpensesSchema(many=True))
    def get(self, id):
        expenses = ExpenseModel.query.filter_by(created_by=id).all()
        return expenses
    
@expensesBlp.route("/expenses/unsettled", methods=["GET"])
class UnsettledExpenses(MethodView):
    @jwt_required()
    @expensesBlp.response(200, ExpensesSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        expenses = user.expenses

        unsettled_expenses = []

        for expense in expenses:
            expenseInDB = ExpenseModel.query.filter_by(id=expense.id).first()
            expenseDetailsInDB = expenseInDB.expense_details

            for expense_detail in expenseDetailsInDB:
                if expense_detail['user_id'] == user_id and not expense_detail['settled']:
                    unsettled_expenses.append(expense)

        return unsettled_expenses
