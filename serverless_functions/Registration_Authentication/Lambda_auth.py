'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Handles user authentication using AWS Cognito
'''
import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64

COGNITO_USER_POOL_ID = 'us-east-1_KINLM8PpJ'
COGNITO_APP_CLIENT_ID = '3dbln0qqhfdvdh2ca8ar7q53o6'
COGNITO_APP_CLIENT_SECRET = '1i6ri5acd5kp1l7nvjmpvculhsbr0i1kea5i5nvuuu37b09tl88q'


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
    data = event
    keys = data.keys()
    # check request body for email and password fields
    if ('email' not in keys) or ('password' not in keys):
        body['error'] = 'Request missing parameters!'
        response = make_response(400, headers, json.dumps(body))
        return response

    # Retrieving user data
    email = data['email']
    password = data['password']

    # check for empty fields
    if (email == '') or (password == ''):
        body['message'] = 'Form contains empty fields!'
        response = make_response(400, headers, json.dumps(body))
        return response

    try:
        cognito = boto3.client('cognito-idp')
        authenticate = {'USERNAME': email, 'PASSWORD': password,
                        "SECRET_HASH": retrieve_sHash(email)}
        resp_auth = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH', AuthParameters=authenticate, ClientId=COGNITO_APP_CLIENT_ID)
        accessToken = resp_auth['AuthenticationResult']['AccessToken']
        userData = cognito.get_user(AccessToken=accessToken)

        # Fetching user's email and security question
        user = {}
        for obj in userData['UserAttributes']:
            key = obj['Name']
            value = obj['Value']
            user[key] = value

        user = {'email': user['email'], 'question': user['custom:question']}
        body['userData'] = {
            'accessToken': accessToken,
            'user': user
        }
        response = make_response(200, headers, json.dumps(body))
        return response
    except cognito.exceptions.UserNotFoundException as e:
        body['error'] = 'User not found!'
        response = make_response(401, headers, json.dumps(body))
        return response
    except cognito.exceptions.NotAuthorizedException as e:
        body['error'] = 'Not authorized!'
        response = make_response(401, headers, json.dumps(body))
        return response
    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
