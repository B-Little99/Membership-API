from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from passwords import PasswordHashing
import json, time

# Initial set up for the API and DB
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# DB Model set up
class EmployeeAccountsModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    employeeID = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    mobileNumber = db.Column(db.String(200), nullable = False)
    accountBalance = db.Column(db.Integer, nullable = False)
    pinPassword = db.Column(db.String(100), nullable = False)

    # Method to represent objects as a string
    def __repr__(self):
        return f"Employee Account (employeeID = {employeeID}, name = {name}, email = {email}, mobileNumber = {mobileNumber}, accountBalance = {accountBalance}, pin = {pinPassword})"

# Used the below to intialise or drop the database as needed.
# db.drop_all()
# db.create_all()

# resource fields to serialise the data that we get from the DB 
# using the marshal_with() decorator so data is in a readable format
resource_fields = {
    'id': fields.Integer,
    'employeeID': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'mobileNumber': fields.String,
    'accountBalance': fields.Integer,
    'pinPassword': fields.String
}

# Set up for the employee registration arguments required, using the request parser object.
collectionPostArgs = reqparse.RequestParser()
collectionPostArgs.add_argument("employeeID", type = int, help = "ID of the employee is required.", required = True)
collectionPostArgs.add_argument("name", type = str, help = "Name of the employee is required.", required = True)
collectionPostArgs.add_argument("email", type = str, help = "Your email is required", required = True)
collectionPostArgs.add_argument("mobileNumber", type = str, help = "Your mobile number is required", required = True)
collectionPostArgs.add_argument("pinPassword", type = str, help = "Your account pin password is required.", required = True)

# Set up for the employee list arguments required, using the request parser object.
collectionGetArgs = reqparse.RequestParser()
collectionGetArgs.add_argument("employeeID", type = int, help = "ID of the employee is required.", required = True)
collectionGetArgs.add_argument("pinPassword", type = str, help = "Your account pin password is required.", required = True)

# Set the class for the employees collection endpoint '/employees'
class EmployeesCollection(Resource):

    # This is the method that an admin can call to see all employees for admin work
    @marshal_with(resource_fields)
    def get(self):
        # thread = threading.Thread(target=callTimeout).start()
        arguments = collectionGetArgs.parse_args()
        employee = EmployeeAccountsModel.query.filter_by(employeeID = arguments['employeeID']).first()
        
        if employee:
            # global stopThread
            # stopThread = True

            storedHash = employee.pinPassword
            verification = PasswordHashing.verifyHash(storedHash, arguments['pinPassword'])

            if verification == True:
                
                queryResult = EmployeeAccountsModel.query.all()
                return queryResult, 200
            else:
                return {"httpCode": 400, "message": "You need to provide a correct pin password to proceed."}

    # This is the post method that the client will call when an 
    # employee wants to register their new details 
    def post(self): 
        arguments = collectionPostArgs.parse_args()
        result = EmployeeAccountsModel.query.filter_by(employeeID = arguments['employeeID']).first()
        
        # if the employee account / result is found it throws an error as new accounts should not already be registered
        if result:
            abort(404, message="This employee is already registered.")
        newPassword = PasswordHashing.hashPassword(arguments['pinPassword'])

        employee = EmployeeAccountsModel(employeeID = arguments['employeeID'], name = arguments['name'], email = arguments['email'], mobileNumber = arguments['mobileNumber'], accountBalance = 0, pinPassword = newPassword)
        db.session.add(employee)
        db.session.commit()
        return {"httpCode": 201, "message": "Thank you for registering your new account."}

# The below sets the endpoint and what class to use
api.add_resource(EmployeesCollection, "/api/V1/employees")

# Set up for the individual employee GET arguments required that will provide the welcome/goodbye message.
resourceGetArgs = reqparse.RequestParser()
resourceGetArgs.add_argument("employeeID", type = int, help = "ID of the employee is required to retrieve the account.", required = True)
resourceGetArgs.add_argument("context", type = str, help = "You must provide a context to get the appropriate response", required = True)
resourceGetArgs.add_argument("pinPassword", type = str, help = "Your account pin password is required.", required = True)

# Set up for the individual employee PUT arguments required that will enable an employee to update their details.
resourcePutArgs = reqparse.RequestParser()
resourcePutArgs.add_argument("employeeID", type = int, help = "ID of the employee is required to retrieve the account.", required = True)
resourcePutArgs.add_argument("pinPassword", type = str, help = "Your account pin password is required.", required = True)
resourcePutArgs.add_argument("funds", type = int, help = "The amount of money to be deposited/withdrawn is required", required = True)
resourcePutArgs.add_argument("fundType", type = str, help = "the type of transaction is required and should be either a 'withdraw' or a 'deposit' so we can differentiate between the action. ", required = True)

# Set the class for the specific employees endpoint '/employees/<int:employeeID>'
class EmployeesResource(Resource):

    # The GET method that provides the custom welcome message or the goodbye message depending on the context provided by the client.
    # When the context is a welcome message it will find the employee in the DB, verify the password and return the message.
    def get(self, employeeID):
        arguments = resourceGetArgs.parse_args()

        if arguments['context'] == 'welcomeMessage':
            # The below finds the specified employee and stores th user name and hash
            result = EmployeeAccountsModel.query.filter_by(employeeID = employeeID).first()
            userName = result.name
            storedHash = result.pinPassword
            # if the employee account / result cannot be find then a 404 error occurs.
            if not result:
                abort(404, message = "You are not registered on the system yet. Please sign up to create an account.")

            # This verification compares hashes.
            verification = PasswordHashing.verifyHash(storedHash, arguments['pinPassword'])

            # After verifying the password is true I create the success object and update it with the custom message to include the name
            if(verification == True):
                successObject = {"httpCode": 200}
                messageText = "Welcome to your account {name}.".format(name = userName)
                successObject.update({"message": messageText})
                return successObject
            else:
                return abort(404, message = "That password is wrong.")
        elif arguments['context'] == 'goodbyeMessage':
                successObject = {"httpCode": 200, "message": "Goodbye."}
                return successObject
        else:
            return {"httpCode": 400, "message": "You need to provide a correct contextual value."}

    # The PUT method that the client will call to update the account balance 
    def put(self, employeeID):
        # ensures the arguments are provided then tries to get the employee account in the DB
        arguments = resourcePutArgs.parse_args()
        result = EmployeeAccountsModel.query.filter_by(employeeID = employeeID).first()
        if not result:
            abort(404, message = "That employee ID does not exist yet.")

        storedHash = result.pinPassword
        verification = PasswordHashing.verifyHash(storedHash, arguments['pinPassword'])

        if(verification == True):
            if arguments['fundType'] == 'withdraw':
                # Starts the calculation to withdraw the funds provided
                # Withdraw is only successful if the new balance variable will be more than/equal to 0, because that means they can afford what they are buying.
                withdrawValue = arguments['funds']
                newBalance = result.accountBalance - withdrawValue

                if newBalance >= 0:
                    result.accountBalance = newBalance
                    db.session.commit()
                    return {"httpCode": 200, "message": "Request successful. The account has been updated."}
                    
                elif newBalance < 0:
                    return {"httpCode": 400, "message": "Bad request. The account could not be updated as the account balance would be less than 0."}
            
            elif arguments['fundType'] == 'deposit':
                # Starts the calculation to add the funds
                # Deposit is only successful if the balance is more than/equal to 0, which should always evaluate to true if they are adding money.
                depositValue = arguments['funds']
                newBalance = result.accountBalance + depositValue
                if newBalance >= 0:
                    result.accountBalance = newBalance
                    db.session.commit()
                    return {"httpCode": 200, "message": "Request successful. The money has been deposited."}
                elif newBalance < 0:
                    return {"httpCode": 400, "message": "Bad request. The account could not be updated as the account balance would be less than 0."}
            else:
                return {"httpCode": 400, "message": "Bad Request. The client must authenticate itself with a correct fund type to get a response."}
        
        else:
            return abort(404, message="That password is wrong.")

# Add the endpoint to the EmployeesResource class
api.add_resource(EmployeesResource, "/api/V1/employees/<int:employeeID>")

class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello world!"}

api.add_resource(HelloWorld, "/api/V1/helloworld")

# This snippet is what runs the python code when its run from the command line.
# Debug=True needs to be turned off for deployment
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0")
