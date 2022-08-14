# Membership-API
This is the original membership API that I created for my level 4 software developer coursework, which attained a distinction. 



[**Words words**](linklink)<br>





## Design
The synoptic project that I am completing is Project E, the RESTful membership system API. The requirements are as follows.
Requirements

From the business requirements provided I created several user stories (including my stories from additional requirements), assumptions and additional requirements that can be seen below.

### User stories

User story
Detail
Acceptance criteria
As an employee,
I want to register my card,
So that I can use my account.
In order to use the kiosk terminals, first the customer must be able to register their card at the terminals for future use. When doing this they will provide a number of personal details to authenticate who they are. They will have a new registered account, but if the wrong data type is used then it will throw an error message.
The personal details to be provided are: their employee ID, full name, company email, a mobile number and their own pin to access the services.
A POST HTTP method will be used, as well as extra information:
Employee ID
Full name
Company email
Mobile number
A pin

This information will be committed to the account database so the employee can use the account in the future.

If the employee provides all of the correct arguments required, it will insert the new details and provide a thank you message.

If the employee is in the company database and in the registered table and tries to re-register, it will come up with an error message to explain they already have an account.

At all stages of the POST method appropriate HTTP status codes will be returned.
As an employee,
I want to top up or use account credit,
So that I can buy food.
In order for a registered account to use the kiosk terminals to top up the account, they will need to be able to top up or withdraw credit from their account in order to purchase food or add more credit.
A PUT HTTP method will be used, and will require the following parameters:
Employee ID - for identification of what account to update
Funds - to know what value to update with
Fund type - to know if the funds should be added or taken away from the account
Pin password for security

The PUT method will also mean the new value of the account balance is committed to the database.

In addition to the above, there should also be appropriate error messages. In the instance that the employee ID is not registered in the database when trying to make a transaction, it should error out with a custom message to alert the user to register first.

If the employee is trying to buy food that is more than the account balance for their account, then it will error out and let the customer know they do not have the funds to complete the transaction. 

Appropriate status codes will be provided for both correct and incorrect usage of the API.
As an employee,
I want a custom welcome message, 
So that I know I have logged into the system.
For the customer to be certain they have correctly tapped their card onto the kiosk, it should provide a custom welcome message that features their name. 
A login message should appear in the format: “Welcome to your account {name}.”, before allowing the employee to continue with an action.


As an employee,
I want a goodbye message 
So I know I have logged out of the kiosk.
For the customer to know they have logged out correctly, they should see a goodbye message.
When the kiosk makes a second call with appropriate information being provided, the following logout message should appear: “Goodbye.” After this point another employee can use the kiosk terminal.
As an employee,
I want the system to timeout,
So if I forget to log out nobody will use my credit.
If an employee forgets to tap their registered card a second time, then there needs to be a timeout after 2 minutes of no activity (no server activity).
After 240 seconds of no activity (no response from the server for the specified action) the kiosk will time out ready for the next user to log in.
As an admin,
I want to see all registered employees,
So I can carry out admin duties.
In order for the product to be maintained, it needs to allow functionality for an admin with higher privileges to access all the data (with pagination too). This will allow the admin role to keep an accurate record of the registered employees.
A GET HTTP method will be used on the registered accounts database table, in order to retrieve and format the employee information in a set format for the admin to view. A pin password will be required. A 2xx HTTP status code will be returned with the results (which will be attained through a database query). 
As a developer,
I want to dockerise this product,
So functionality can be reused across systems in the future.
In the future the company that develops this solution may get other contracts to interface with systems, so it will need to work across operating systems in an isolated environment with all its dependencies.
An appropriate docker file will be created, and the docker file will be built to test that the containerised app will run.
As a employee, 
I want my account password to be secure,
So that nobody else can access my information
In order to ensure the security of the employee accounts we need to be able to use an algorithm to encrypt employee password data. This would mean that the password needs to be salted with an additional word and then hashed using a strong hash function.
When registering a new account the password pin provided by the employee will be salted and hashed using the SHA-256 hashing algorithm, submitting the hashed value to the database. When a user tries to log in it will then go through a verification process where it takes in the pin and hashes it and compares it to the stored hash value to determine if the password is correct or not.



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


#### Extra assumptions
It is not explicitly clear if the existing IT department is handling the updating of account balances through the API or not. It would seem illogical to have a RESTful API for registering and topping up money without the ability to top up and use the money on the account. 

What I assume is meant by the background information is that the existing IT department will handle how any physical money is registered on the kiosk client side. From the business requirements, it states they want a RESTful web service for registering and topping up money, so I assume they still want the functionality to update account balances. 

Another assumption made is that there is some kind of ‘all employees’ database tables that contains the details of every employee that is maintained, which could be used as part of the verification process using the employee ID. For example, this table will allow an extra security layer when authenticating if an employee is real or not.

### Additional requirements
There are also several additional requirements that I created for this project and added to the user stories.

#### The admin role
One additional requirement is the admin role, with functionality to view data using the API. I added this requirement, because it will help maintain an accurate record of information relating to the employees that are registered. It can be reasonably expected that in any organisation there will be an admin who works using/maintaining information related to systems and staff, so this could prove to be very important.

#### Password salt/hashing
Another additional requirement I have added is the secure hashing and salting of passwords, so that they are not stored in plain text which is bad security practice. This will ensure that we use a high quality SHA algorithm and salt the password before hashing so that people's accounts can be more secure than if they were in plain text. This will ensure that the security non-functional requirement can be addressed.

### Non functional requirements
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








