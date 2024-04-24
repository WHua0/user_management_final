# IS601 Final: User Management

## Learnings & Experiences

## Dockerhub

![Dockerhub Repository](submissions/Dockerhub.png)

## Github Actions

## Github Commit History

## Pytest Coverage

## [QA (Quality Assurance) Issues](https://github.com/WHua0/user_management_final/issues?q=is%3Aissue+is%3Aclosed)

![Github Issues](submissions/Github%20Issues.png)

### [Issue 1: POST / register / Register - New User Email Verification](https://github.com/WHua0/user_management_final/issues/1)
![Github Issue 1](submissions/Github%20Issue%201.png)
![Issue 1 Fix](submissions/Github%20Issue%201%20Fix.png)

A verification email should be sent not before, but after the new user has been commited to the database. Thus, the code was rearranged accordingly.

Clicking the email verification link should only update user role to Authenticated if user role is Anonymous. It should not affect user roles, such as Authenticated, Manager, and Admin. Thus, an if statement was added.

### [Issue 2: POST / register / Register - Nonmatching Response Body](https://github.com/WHua0/user_management_final/issues/3)
![Github Issue 2](submissions/Github%20Issue%202.png)
![Issue 2 Fix](submissions/Github%20Issue%202%20Fix.png)

User role input has no impact, and is automatically set to Anonymous. Thus, role was removed from UserBase. 

The code did not check for existing user with the same nickname in the database, and generated a random nickname regardless of input.

A database check for an existing user with the same nickname was added to the database check for an existing user with the same email. Logging error was also updated to "User with given email or nickname already exists".

HTTP 400 detail message was updated to "Email or Nickname already exists".

An if statement was added to generate nickname, such that a new nickname would be generated and used only if no nickname is provided. 

![Issue 2 Test](submissions/Github%20Issue%202%20Test.png)

### [Issue 3: POST / users / Create User - Nonmatching Response Body & Missing Error for Diplicate Nickname](https://github.com/WHua0/user_management_final/issues/5)
![Github Issue 3](submissions/Github%20Issue%203.png)
![Issue 3 Fix](submissions/Github%20Issue%203%20Fix.png)

The code was found to return the incorrect values for is_professional, linkedin_profile_url, and github_profile url.

The missing lines for is_professional, linkedin_profile_url, and github_profile url.was added to UserResponse.model_construct.

The code did not check if existing user with the same nickname already exists in the database. 

A nickname check was added to raise Http 400 if nickname was used by another user.

The email check was updated to reflect user with existing email, rather than just existing user, for clarity. 


![Issue 3 Test](submissions/Github%20Issue%203%20Test.png)

### [Issue 4: GET / users / {user_Id} Get User - Nonmatching Response Body](https://github.com/WHua0/user_management_final/issues/7)
![Github Issue 4](submissions/Github%20Issue%204.png)
![Issue 4 Fix](submissions/Github%20Issue%204%20Fix.png)

The code was found to return the incorrect value for is_professional.

The missing line for is_professional was added to UserResponse.model_construct.

### [Issue 5: PUT / users / {user_id} Update User - Nonmatching Response Body & Missing Error for Duplicate Email and Nickname](https://github.com/WHua0/user_management_final/issues/9)
![Github Issue 5](submissions/Github%20Issue%205.png)
![Issue 5 Fix](submissions/Github%20Issue%205%20Fix.png)

The code was found to return the incorrect value for is_professional.

The missing line for is_professional was added to UserResponse.model_construct.

The code did not check if existing user with the same email or nickname already exists in the database. Furthermore, the check for if the user exists was incorrect, and in the wrong location. The checks should be before the updated data is committed to the database.

The check for if the user exists was updated to search the database for a matching user id, and raise Http 400 if not found.

The checks for a existing email and nickname were also added. However, the checks would only be performed if the user's updated nickname or email does not match the user's current ones. The checks raise Http 400 if nickname or email is already in use by another user.

![Issue 5 Test](submissions/Github%20Issue%205%20Test.png)

### [Issue 6: GET / users / List User - Missing Error for Invalid Skip Integer and Limit Integer Input](https://github.com/WHua0/user_management_final/issues/10)
![Github Issue 6](submissions/Github%20Issue%206.png)
![Issue 6 Fix](submissions/Github%20Issue%206%20Fix.png)

The code does not check the inputs for Skip Integer and Limit Integer. The only error returned is if Limit Integer is 0.

Two if statements was added to list users. If Skip Integer is less than 0, Http 400 is raised. If Limit Integer is not more than 0, Http 400 is raised.

![Issue 6 Test](submissions/Github%20Issue%206%20Test.png)

### [Issue 7: Missing Validators, Max Length, Min Length, etc.](https://github.com/WHua0/user_management_final/issues/15)
![Github Issue 7](submissions/Github%20Issue%207.png)
![Issue 7 Fix](submissions/Github%20Issue%20Fix%207.png)

The code did not check the inputs for many fields, such that edge cases were allowed. For instance, one could register an user with a password of an empty string.

Various validators and constraints, such as minimum length, maximum length, required characters, and invalid characters, were added to each field, enhancing security and preventing edge cases from occuring.

![Issue 7 Test](submissions/Github%20Issue%207%20Test.png)

## New Feature Implementation