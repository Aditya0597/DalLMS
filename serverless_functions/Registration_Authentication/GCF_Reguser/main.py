'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Handles user form validations
'''
from google.cloud import datastore
import requests
import json
import logging
import re
import os


def make_response(statusCode, headers, body):
    response = {
        "statusCode": statusCode,
        "headers": headers,
        "body": body
    }
    return response


def register_user(request):
    body = {}
    headers = {
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Max-Age': '1296000',
        'Content-type': 'application/json'
    }
    LAMBDA_FUNCTION_URI = os.environ.get('LAMBDA_FUNCTION_URI')
    emailRex = re.compile(
        '^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')
    passwordRex = re.compile(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')
    try:
        data = request.get_json()
        if data:
            data_keys = data.keys()
            if ('email' not in data_keys) or ('name' not in data_keys) or ('role' not in data_keys) or ('password' not in data_keys) or ('gender' not in data_keys) or ('question' not in data_keys) or ('answer' not in data_keys) or ('instituteName' not in data_keys):
                body['error'] = 'Request missing parameters!'
                response = make_response(400, headers, json.dumps(body))
                return response
            email = data['email']
            name = data['name']
            password = data['password']
            gender = data['gender']
            answer = data['answer']
            role = data['role']
            question = data['question']
            instituteName = data['instituteName']

            if (email == '') or (name == '') or (password == '') or (gender == '') or (answer == '') or (role == '') or (instituteName == ''):
                body['error'] = 'Form contains empty fields!'
                response = make_response(400, headers, json.dumps(body))
                return response
            if emailRex.match(email) == None:
                body['error'] = 'Invalid Email format!'
                response = make_response(422, headers, json.dumps(body))
                return response
            if passwordRex.match(password) == None:
                body['error'] = 'Password must contain: At least 1 uppercase, At least 1 lowercase, At least 1 special character, and a minimum length of 8!'
                response = make_response(422, headers, json.dumps(body))
                return response
            userData = {
                "email": email,
                "name": name,
                "password": password,
                "gender": gender,
                "question": question,
                "instituteName": instituteName,
                "role": role
            }
            response_post = requests.post(LAMBDA_FUNCTION_URI, data=json.dumps(
                userData), headers={'Content-Type': 'application/json'})
            response_post = response_post.json()
            # Since every error code is >400
            if (response_post['statusCode'] >= 400):
                response = make_response(
                    response_post['statusCode'], headers, response_post['body'])
                return response
            if 'message' in eval(response_post['body']).keys():
                try:
                    # storing user's QA to datstore
                    client = datastore.Client()
                    entity = datastore.Entity(key=client.key('user'))
                    entity.update(
                        {'email': email, 'question': question, 'answer': answer})
                    client.put(entity)
                    body['message'] = 'User registered successfully!'
                    response = make_response(200, headers, json.dumps(body))
                    return response
                except Exception as e:
                    body['message'] = str(e)
                    response = make_response(500, headers, json.dumps(body))
                    return response
            else:
                body['message'] = response['body']['error']
                response = make_response(500, headers, json.dumps(body))
                return response
        else:
            body["error"] = "Request missing parameters one of ['email', 'name', 'password', 'gender', 'question', 'answer', instituteName', 'role']"
            response = make_response(400, headers, json.dumps(body))
            return response
    except Exception as e:
        body['message'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
