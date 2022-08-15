# Membership-API
This is the original membership API that I created for my level 4 software developer coursework, which attained a distinction. 


## Table of contents

- [**Design**](#Design)<br>
   - [**User stories**](#User-stories)<br>
   - [**Assumptions**](#Assumptions)<br>
   - [**Extra assumptions**](#Extra-assumptions)<br>
   - [**Additional requirements**](#Additional-requirements)<br>
   - [**Non functional requirements**](#Non-functional-requirements)<br>
   - [**Diagrams**](#Diagrams)<br>
   - [**Words words**](#linklink)<br>
- [**API documentation**](#API-documentation)<br>
   - [**Overview**](#Overview)<br>
   - [**HTTP methods and endpoints**](#HTTP-methods-and-endpoints)<br>
   - [**Query string parameters**](#Query-string-parameters)<br>
   - [**HTTP status codes used**](#HTTP-status-codes-used)<br>
   - [**Example request and responses**](#Example-request-and-responses)<br>


## Design
The synoptic project that I am completing is Project E, the RESTful membership system API. The requirements are as follows.
Requirements

From the business requirements provided I created several user stories (including my stories from additional requirements), assumptions and additional requirements that can be seen below.

### User stories

| User story | Detail | Acceptance criteria |
| --- | --- | --- |
| As an employee, I want to register my card, so that I can use my account. | In order to use the kiosk terminals, first the customer must be able to register their card at the terminals for future use. When doing this they will provide a number of personal details to authenticate who they are. They will have a new registered account, but if the wrong data type is used then it will throw an error message. | The personal details to be provided are: their employee ID, full name, company email, a mobile number and their own pin to access the services. A POST HTTP method will be used, as well as extra information: Employee ID, Full name, Company email, Mobile number, A pin. This information will be committed to the account database so the employee can use the account in the future. If the employee provides all of the correct arguments required, it will insert the new details and provide a thank you message. If the employee is in the company database and in the registered table and tries to re-register, it will come up with an error message to explain they already have an account. At all stages of the POST method appropriate HTTP status codes will be returned. |
| As an employee, I want to top up or use account credit, so that I can buy food. | In order for a registered account to use the kiosk terminals to top up the account, they will need to be able to top up or withdraw credit from their account in order to purchase food or add more credit. | A PUT HTTP method will be used, and will require the following parameters: Employee ID - for identification of what account to update. Funds - to know what value to update with. Fund type - to know if the funds should be added or taken away from the account. Pin password for security. The PUT method will also mean the new value of the account balance is committed to the database. In addition to the above, there should also be appropriate error messages. In the instance that the employee ID is not registered in the database when trying to make a transaction, it should error out with a custom message to alert the user to register first. If the employee is trying to buy food that is more than the account balance for their account, then it will error out and let the customer know they do not have the funds to complete the transaction. Appropriate status codes will be provided for both correct and incorrect usage of the API. |
| As an employee, I want a custom welcome message, so that I know I have logged into the system. | For the customer to be certain they have correctly tapped their card onto the kiosk, it should provide a custom welcome message that features their name. | A login message should appear in the format: “Welcome to your account {name}.”, before allowing the employee to continue with an action. |
| As an employee, I want a goodbye message, so I know I have logged out of the kiosk. | For the customer to know they have logged out correctly, they should see a goodbye message. | When the kiosk makes a second call with appropriate information being provided, the following logout message should appear: “Goodbye.” After this point another employee can use the kiosk terminal. |
| As an admin, I want to see all registered employees, so I can carry out admin duties. | In order for the product to be maintained, it needs to allow functionality for an admin with higher privileges to access all the data (with pagination too). This will allow the admin role to keep an accurate record of the registered employees. | A GET HTTP method will be used on the registered accounts database table, in order to retrieve and format the employee information in a set format for the admin to view. A pin password will be required. A 2xx HTTP status code will be returned with the results (which will be attained through a database query). |
| As a developer, I want to dockerise this product, so functionality can be reused across systems in the future. | In the future the company that develops this solution may get other contracts to interface with systems, so it will need to work across operating systems in an isolated environment with all its dependencies. | An appropriate docker file will be created, and the docker file will be built to test that the containerised app will run. |
| As a employee, I want my account password to be secure, so that nobody else can access my information | In order to ensure the security of the employee accounts we need to be able to use an algorithm to encrypt employee password data. This would mean that the password needs to be salted with an additional word and then hashed using a strong hash function. | When registering a new account the password pin provided by the employee will be salted and hashed using the SHA-256 hashing algorithm, submitting the hashed value to the database. When a user tries to log in it will then go through a verification process where it takes in the pin and hashes it and compares it to the stored hash value to determine if the password is correct or not. |


### Assumptions
I assume that the web service paradigm REST has been chosen for its various benefits as follows. REST promotes loosely coupling the client and server, which can make it harder for malicious actors to attempt to use or abuse server resources. REST typically uses less bandwidth, making it more cost effective than alternatives like SOAP (which has a much higher overhead from using XML). 

Another reason RESTful web services are used is because they are stateless, where the server will not remember prior requests/store them and the client has to pass all required information for the request to be understood. Being stateless means the RESTful web service will be less complex, as it does not require server side logic.

Assuming that they want to use REST could also infer that they have a more modern technology stack, possibly without legacy code limitations.

Since this RESTful web service needs to follow industry standards, I assume it will adhere to the following REST industry standards: 

- Appropriate documentation - good, concise documentation is key to any RESTful web service, because it will be relied on by the developers utilising it.
- Stateless requests - by default RESTful web services should be stateless, where they do not store requests made and need the information passed to them from the client.
- Appropriate Uniform Resource Identifiers (URI) structure and names - RESTful web services should follow a predictable structure of URI or ‘Resources’ so that it is easy to follow and use. RFC3986 highlights the use of spinal-case for URIs. Endpoints should be named as nouns not verbs, such as /employees/1 over /getEmployees/1.
- HTTP method use - the HTTP verbs (POST, GET etc.) should be used to describe what is going to happen to resources on the API. So GET should be used to retrieve information from the server, POST should be used to send new data to a server, PUT should be used for updating information. 
- HTTP status codes - when there is an error/action, either on the server side or the client side, there should be appropriate and meaningful use of HTTP status codes, such as 2xx codes for successful requests, 4xx codes for client errors and 5xx codes for server errors.


### Extra assumptions
It is not explicitly clear if the existing IT department is handling the updating of account balances through the API or not. It would seem illogical to have a RESTful API for registering and topping up money without the ability to top up and use the money on the account. 

What I assume is meant by the background information is that the existing IT department will handle how any physical money is registered on the kiosk client side. From the business requirements, it states they want a RESTful web service for registering and topping up money, so I assume they still want the functionality to update account balances. 

Another assumption made is that there is some kind of ‘all employees’ database tables that contains the details of every employee that is maintained, which could be used as part of the verification process using the employee ID. For example, this table will allow an extra security layer when authenticating if an employee is real or not.

### Additional requirements
There are also several additional requirements that I created for this project and added to the user stories.

#### The admin role
One additional requirement is the admin role, with functionality to view data using the API. I added this requirement, because it will help maintain an accurate record of information relating to the employees that are registered. It can be reasonably expected that in any organisation there will be an admin who works using/maintaining information related to systems and staff, so this could prove to be very important.

#### Password salt/hashing
Another additional requirement I have added is the secure hashing and salting of passwords, so that they are not stored in plain text which is bad security practice. This will ensure that we use a high quality SHA algorithm and salt the password before hashing so that people's accounts can be more secure than if they were in plain text. This will ensure that the security non-functional requirement can be addressed.

### Non-functional requirements
There are also a number of non-functional requirements that impact the successful delivery of the solution. The non-functional requirements enable developers to know how a system should work, whereas functional requirements describe what a system should do.

#### Performance
Performance is an incredibly important non-functional requirement in this product. This is because the performance of the API determines how quickly it can return results, which is important when the client is serving customers in real time. Because of this it needs to submit and receive requests with little to no latency and be able to scale with increasing workloads as the company grows too.

In order to address this in the design, I would incorporate some kind of caching system where frequently accessed data is stored along the request response pathway. By doing this it means that each request will first check the appropriate caches for the data, which can help improve performance. 

#### Security
Security is a big non-functional requirement for any project, especially when dealing with monetary transactions. If a malicious actor were to get hold of personally identifiable data, it would be a data breach which could cause fines for breaking GDPR. The malicious actor could also abuse the API so that the cost of request-response transactions from calling the API significantly increased, posing a financial threat.

In the design of the API it could be addressed by utilising different methods, such as rate limiting to stop a DDoS attack, using encryption such as TLS and OAuth tokens to authenticate users so it's clear they are actual users of the system and not a spoof account. Another layer of security could be by hashing and salting passwords so that the pins cannot be brute forced by a malicious user. 

#### Reliability
Reliability comes down to how long the system can operate without failures. This is important because when multiple systems are utilising an API, a user base needs it to operate as close to 100% during the operating times of the overall system. If a system had low reliability (e.g. short time between failures) then that could impact the service level agreements or targets set by the team/company. If the API is not reliable in this instance it ultimately means a poor customer service and could lead to complaints and an unhappy workforce.

Ways to deal with this include implementing an effective logging and monitoring system in place, so that we can track and look for when the API is failing to try and improve it. 



### Diagrams
From the above requirements I made the following diagrams. 


The above diagram showcases the use cases for the requirements and what users should be able to do in their respective roles. 


The above diagram shows a high level overview of the relationship between the client, the API and the server. It shows that requests go from the client, through the API to the server and the response is returned through the API and back to the client. 


The workflow shows more specifically the route that a request should go through within the API, detailing some of the functionality and how it should work.

Initially there is the request from the client which should contain the appropriate information to fulfil the request, then the API determines if the client is authorised and if the request is okay. If either of these come back as false, then it will error out and the client can retry the request. If everything is fine then the API will sanitise and validate input as a security measure. Then It should check if there is any cached data that could be used (which will help on performance), and return the data and appropriate success code if there is cached data. If however, there is no appropriate cached data then it will contact the server table and find the appropriate information, which will then allow the API to create an appropriate response following a JSON format. The API will then return the data and a success code to complete the call. 



The above data model shows how the database should be constructed and what data is stored. Ideally, we would have access to the company employees database which we can use to verify the identity of a person trying to register a new account. The registered accounts table represents the new table that will be created.


## API documentation
This section discusses the results of my work, including the limitations of the design/implementation, the proposed future improvements and a user guide for developers. 

- [**Overview**](#Overview)<br>
- [**HTTP methods and endpoints**](#HTTP-methods-and-endpoints)<br>
- [**Query string parameters**](#Query-string-parameters)<br>
- [**HTTP status codes used**](#HTTP-status-codes-used)<br>
- [**Example request and responses**](#Example-request-and-responses)<br>


### Limitations
Any initial release of a product will have its own limitations. With this API the limitations range from a lack of monitoring to security based limitations.

One limitation is the docker container does not run due to the external passwords.py file import blocking the container from running, because it expects password to be a module when I am actually trying to import another file. This issue will need to be investigated as a future improvement. Due to the time constraints the timeout is not on every HTTP method, which will need to be expanded in the future so it is implemented on every HTTP method for the API.

One area of limitation is security. While the API supports salting and hashing of passwords, it does not currently support multi-factor authentication, which can pose a security risk when utilising a public facing endpoint like with APIs as there is one less authentication layer. There are multiple attacks that can be done to harm an API or its company, such as DDoS attacks. These types of malicious attacks can be protected against by rate limiting (setting the max API calls within a specified time) to manage network traffic better, but this is not implemented in the current design which could lead to a cyber attack.

At this point in time there are no caching abilities, due to the limited timeframe. This would be a great addition to the API, because it could provide a smoother customer journey so that common information can be stored and used before attempting to contact the host server. This would result in quicker results being provided and lower API latency, but because it is not yet implemented it could decrease overall performance slightly.

The data format provided is only in JSON. It would be ideal to also include XML and potentially CSV, as it could mean that if an old legacy system needed to use the API it would have an easier time working with the API.

Another limitation is that at this current point there are no monitoring/analytics that gather data behind the usage of the API. This could be important to the business to see uptake of the API and therefore the service and could also help determine where there are errors, which could be used to improve the service further.



### Future improvements
With any project, there are always improvements that could be made. These improvements can be categorised into immediate (actions that require prompt delivery for functionality/security upgrades), short term (actions that will not take much time to investigate), medium term (actions that may require some time to investigate) and long term (actions that will take a considerable amount of time to research) improvements.

**Immediate improvements**

*Add admin authorisation*

An immediate improvement would be to add an extra database table for admin credentials to be stored. It could be used in conjunction with a registered account password for access to the collection GET method to view all employees. This provides extra security through an added authorisation layer. There should also be extra methods to provide more use to admins, such as a DELETE and PUT method so that the admins can do more to administer the kiosk account information.

*Implement wider timeout usage and investigate docker issues*

More immediate improvements include the implementation of the timeout function across all HTTP methods and investigating the docker issues, so that I can run the API on docker containers.

*Clarify the business requirements*

Another improvement would be to clarify requirements with a business stakeholder. It seemed unclear if the product should include a method to update account balances, as requirements stated the product should be used to register and top up with money. However, it mentioned the IT team handling transactions. By understanding from transparency and clarity what they want, we can remove the functionality or keep it to keep the code clean.

*Document more programming language examples*

An immediate task that would improve the product is by adding additional programming languages to the documentation, as this would cater to a wider range of technical abilities within the company and make it more usable for the customer developers.

**Short term improvements**

*Set up a feedback meeting*

One of the short term improvements would be to hold a feedback meeting with the first catering IT developers to gather their input and find out any outstanding issues. This can be used to inform the product backlog for the API. 

*Implement caching*

Another improvement that would have a big impact is setting up a caching system, so that the most commonly requested HTTP methods can be stored so future requests can be serviced more efficiently than just sending the request to the server. This would improve the efficiency and latency of the API.

*Set up rate limiting*

To ensure that the API service does not get overwhelmed and cause performance issues a good short term improvement would be to enforce a request limit, so that only requests coming from the company IP address will be valid. This would mean that any external requests would not proceed. 

**Medium term improvements**

*Set up API monitoring*

Implementing a monitoring system so that data can be gathered about the use metrics of the API, which can be analysed and fed into the continued improvement and development of the API as part of the company API strategy. The data could be used to inform the API strategy or it could be used to set one up.

*Security review*

After more improvements have been made to the API and there is a more stable version available, then there should be a full security review. This review would include looking at the top 10 security vulnerabilities for APIs and seeing if the developed product could be susceptible to these security issues. 

**Long term improvements**

*Implement AI analysis*

One long term improvement would be to implement AI analysis on monitoring systems that  have gathered data on the API usage, for predicting future usage but also to help detect suspicious activity that could be a malicious attack by a third party.

*Create a face recognition system*

A significant improvement for the long term versioning of this API would be to create a face recognition system, so that it would improve the security and verify the person trying to do something with their account.


### API V1 User Guide


#### Overview
The First Catering Membership API V1 is the first version of a RESTful web service that works on a predictable URI structure. The API returns structured JSON data or appropriate error messages, through the use of HTTP verbs across the two main endpoints (/employees and /employees/<int:employeeID>).

Please note, that this API does not support trailing backslashes at the end of requests.


#### HTTP methods and endpoints


#### Query string parameters


#### HTTP status codes used


#### Example request and responses


**GET /api/V1/helloworld**

Example curl:
```
curl --location --request GET 'http://127.0.0.1:5000/api/V1/helloworld'
```
Example response:
```
{
    "data": "Hello world!"
}
```


**Register a new account**

Example curl:
```
curl --location --request POST 'http://127.0.0.1:5000/api/V1/employees?id=88&employeeID=88&name=post tester&email=test@url.com&mobileNumber=07415074042&accountBalance=0&pinPassword=1234'
```
Example response:
```
{
    "httpCode": 201,
    "message": "Thank you for registering your new account."
}
```


**Get a list of all employees**

Example curl:
```
curl --location --request GET 'http://127.0.0.1:5000/api/V1/employees?employeeID=88&pinPassword=1234'
```
Example response:
```
[
    {
        "id": 1,
        "employeeID": 19,
        "name": "Test Name",
        "email": "test@url.com",
        "mobileNumber": "07415293847",
        "accountBalance": 0,
        "pinPassword": "$pbkdf2-sha256$29000$zllrbS3F.F/L.X8v5TwnJA$ISR9gzDuoKZKNuzMECXsdhFmqDKEyV.TK.4xeaAC2Eo"
    },
    {
        "id": 2,
        "employeeID": 10,
        "name": "Test Name",
        "email": "test@url.com",
        "mobileNumber": "07415293847",
        "accountBalance": 0,
        "pinPassword": "$pbkdf2-sha256$29000$OUfIWUvpXQvBmFNKaY1Rag$wRRpccdAFFw3wHyWR5UjAPktDbB3iIuN/fouZNUA7IY"
    },
    {
        "id": 3,
        "employeeID": 11,
        "name": "Test Name",
        "email": "test@url.com",
        "mobileNumber": "07415293847",
        "accountBalance": 0,
        "pinPassword": "$pbkdf2-sha256$29000$6T1nDCGk9P6/t9Z6b22tNQ$mpDO4DC.xHVmmk/pLnXonUjlpVa4n3YLkjs5byj.0fM"
    }
]
```


**Custom login message**

Example curl:
```
curl --location --request GET 'http://127.0.0.1:5000/api/V1/employees/66?employeeID=66&pinPassword=1234&context=welcomeMessage'
```
Example response:
```
{
    "httpCode": 200,
    "message": "Welcome to your account NEW Little."
}
```


**Goodbye message**

Example curl:
```
curl --location --request GET 'http://127.0.0.1:5000/api/V1/employees/66?employeeID=66&pinPassword=1234&context=goodbyeMessage'
```
Example response:
```
{
    "httpCode": 200,
    "message": "Goodbye."
}
```


**Deposit to account balance**

Example curl:
```
curl --location --request PUT 'http://127.0.0.1:5000/api/V1/employees/19?employeeID=19&pinPassword=4321&funds=200&fundType=deposit'
```
Example response:
```
{
    "httpCode": 200,
    "message": "Request successful. The account has been updated."
}
```


**Purchase with account balance**

Example curl:
```
curl --location --request PUT 'http://127.0.0.1:5000/api/V1/employees/19?employeeID=19&pinPassword=4321&funds=150&fundType=withdraw'
```
Example response:
```
{
    "httpCode": 200,
    "message": "Request successful. The account has been updated."
}
```
