# IS601 Final: User Management

## Learnings & Experiences

## Dockerhub

## Github Actions

## Github Commit History

## Pytest Coverage

## [QA (Quality Assurance) Issues](https://github.com/WHua0/user_management_final/issues?q=is%3Aissue+is%3Aclosed)

### [Issue 1: POST / register / Register - New User Email Verification](https://github.com/WHua0/user_management_final/issues/1)
![Github Issue 1](submissions/Github%20Issue%201.png)
![Issue 1 Fix](submissions/Github%20Issue%201%20Fix.png)

A verification email should be sent not before, but after the new user has been commited to the database.

Clicking the email verification link should only update user role to Authenticated if user role is Anonymous. It should not affect user roles, such as Authenticated, Manager, and Admin.

### [Issue 2: POST / register / Register - Nonmatching Response Body](https://github.com/WHua0/user_management_final/issues/3)
![Github Issue 2](submissions/Github%20Issue%202.png)

### [Issue 3: POST / users / Create User - Nonmatching Response Body & Missing Error for Diplicate Nickname](https://github.com/WHua0/user_management_final/issues/5)
![Github Issue 3](submissions/Github%20Issue%203.png)

### [Issue 4: GET / users / {user_Id} Get User - Nonmatching Response Body](https://github.com/WHua0/user_management_final/issues/7)
![Github Issue 4](submissions/Github%20Issue%204.png)

### [Issue 5: PUT / users / {user_id} Update User - Nonmatching Response Body & Missing Error for Duplicate Email and Nickname](https://github.com/WHua0/user_management_final/issues/9)
![Github Issue 5](submissions/Github%20Issue%205.png)

### [Issue 6: GET / users / List User - Missing Error for Invalid Skip Integer and Limit Integer Input](https://github.com/WHua0/user_management_final/issues/10)
![Github Issue 6](submissions/Github%20Issue%206.png)

### [Issue 7: Missing Validators, Max Length, Min Length, etc.](https://github.com/WHua0/user_management_final/issues/15)
![Github Issue 7](submissions/Github%20Issue%207.png)

## New Feature Implementation