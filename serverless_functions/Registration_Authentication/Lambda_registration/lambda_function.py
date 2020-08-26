'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Handles user registration using AWS Cognito
'''
import boto3
import botocore.exceptions
import json
import pymysql
import hmac
import hashlib
import base64

# Cognito User-Pool Information
COGNITO_USER_POOL_ID = 'us-east-1_KINLM8PpJ'
COGNITO_APP_CLIENT_ID = '3dbln0qqhfdvdh2ca8ar7q53o6'
COGNITO_APP_CLIENT_SECRET = '1i6ri5acd5kp1l7nvjmpvculhsbr0i1kea5i5nvuuu37b09tl88q'

# Function to get the secret hash


def retrieve_sHash(email):
    message = email + COGNITO_APP_CLIENT_ID
    digest = hmac.new(str(COGNITO_APP_CLIENT_SECRET).encode(
        'utf-8'), msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    decode = base64.b64encode(digest).decode()
    return decode


def make_response(statusCode, headers, body):
    response = {
        "statusCode": statusCode,
        "headers": headers,
        "body": body
    }
    return response


def lambda_handler(event, context):
    body = {}
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Content-Type'] = 'application/json'
    # Connection to the AWS-RDS
    try:
        connection = pymysql.connect(host='serverless.cljjsiiqwmmz.us-east-1.rds.amazonaws.com',
                                     user='*****', password='*****', db='**********', charset='utf8mb4')
        cursor = connection.cursor()
    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
    # Getting the user data
    data = event
    email = data['email']
    name = data['name']
    password = data['password']
    gender = data['gender']
    question = data['question']
    role = data['role']
    instituteName = data['instituteName']
    # Using Boto3 Cognito client
    try:
        cognito = boto3.client('cognito-idp')
        cognito.sign_up(ClientId=COGNITO_APP_CLIENT_ID, SecretHash=retrieve_sHash(email), Username=email, Password=password,  UserAttributes=[{'Name': "email", 'Value': email}, {
                        'Name': 'name', 'Value': name}, {'Name': 'gender', 'Value': gender}, {'Name': 'custom:question', 'Value': question}], ValidationData=[{'Name': "email", 'Value': email}])

    except cognito.exceptions.UsernameExistsException as e:
        body['error'] = "The account already exists!"
        response = make_response(409, headers, json.dumps(body))
        return response

    except cognito.exceptions.InvalidPasswordException as e:
        body['error'] = "Invalid Password!"
        response = make_response(422, headers, json.dumps(body))
        return response

    except cognito.exceptions.NotAuthorizedException as e:
        body['error'] = "Not authorized!"
        response = make_response(401, headers, json.dumps(body))
        return response

    except cognito.exceptions.UserLambdaValidationException as e:
        body['error'] = str(e)
        response = make_response(409, headers, json.dumps(body))
        return response

    except cognito.exceptions.InternalErrorException as e:
        body['error'] = "Internal server error!"
        response = make_response(500, headers, json.dumps(body))
        return response

    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response

    try:
        cursor.execute(
            f"INSERT INTO user_reg (name, email, institute, gender, role) VALUES ('{name}', '{email}', '{instituteName}', '{gender}', '{role}');")
        connection.commit()
        connection.close()
        body["message"] = "Successfully Registered User!"
        response = make_response(200, headers, json.dumps(body))
        return response

    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
