import requests

# This is a test file that I would use to complete different actions throughout testing and development.

# Base URL for testing 
BASE = "http://127.0.0.1:5000"

# Random sample data.
data = [
    {"id": 9, "employeeID": 66, "name": "NEW John", "email": "test@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "1234"},
    {"id": 10, "employeeID": 19, "name": "Jim J", "email": "test@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "4321"},
    {"id": 2, "employeeID": 10, "name": "John James", "email": "rest@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "1234"},
    {"id": 3, "employeeID": 11, "name": "James John", "email": "te@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "1234"},
    {"id": 4, "employeeID": 12, "name": "John Smol", "email": "test@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "1234"},
    {"id": 8, "employeeID": 55, "name": "HOPE John", "email": "test@url.com", "mobileNumber": "07445874349", "accountBalance": 0, "pinPassword": "1234"}
]

# Testing to get data into database and POST multiple new registrations at once.
def testDataSubmission():
    for i in range(len(data)):
        response = requests.post(BASE + "/api/V1/employees", data[i])
        print(response.json())

# Test to produce error messaging from arguments parser.
def testEmployeeArguments():
    response = requests.get(BASE + "/api/V1/employees/19")
    print(response.json())

# Tests I get the employee list back.
def testListEmployees():
    response = requests.get(BASE + "/api/V1/employees", {"employeeID": 19, "pinPassword": "4321"})
    print(response.json())


# Tests I get the welcome message back
def testWelcomeMessage():
    response = requests.get(BASE + "/api/V1/employees/10", {"employeeID": 10, "context":"welcomeMessage", "pinPassword":"1234"})
    print(response.json())

# Tests I get the goodbye message back
def testGoodbyeMessage():
    response = requests.get(BASE + "/api/V1/employees/19", {"employeeID": 10, "context":"goodbyeMessage", "pinPassword":"4321"})
    print(response.json())


# Tests I get the no password message back
def testNoPasswordError():
    response = requests.get(BASE + "/api/V1/employees/19", {"context":"goodbyeMessage"})
    print(response.json())


# Tests I get the collection argument error help text back
def testCollectionArguments():
    response = requests.get(BASE + "/api/V1/employees")
    print(response.json())


# Tests put method for depositing
def testDeposit():
    response = requests.put(BASE + "/api/V1/employees/19", {"pinPassword": "4321", "funds": 200, "fundType": "deposit"})
    print(response.json())

