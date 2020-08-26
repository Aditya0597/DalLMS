'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Handles user authentication using datastore client
'''
from google.cloud import datastore
import json
import pymysql


def make_response(statusCode, headers, body):
    response = {
        "statusCode": statusCode,
        "headers": headers,
        "body": body
    }
    return response


def authenticate(request):
    body = {}
    headers = {
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Max-Age': '1296000',
        'Content-type': 'application/json'
    }
    try:
        connection = pymysql.connect(host='serverless.cljjsiiqwmmz.us-east-1.rds.amazonaws.com',
                                     user='*****', password='*****', db='*****', charset='utf8mb4')
        cursor = connection.cursor()
    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response

    try:
        data = request.get_json()
        if data:
            data_keys = data.keys()
            if ('email' not in data_keys) or ('question' not in data_keys) or ('answer' not in data_keys):
                body['error'] = 'Request missing parameters!'
                response = make_response(400, headers, json.dumps(body))
                return response

            email = data['email']
            answer = data['answer']
            question = data['question']

            if answer == '':
                body['error'] = 'Answer cannot be empty!'
                response = make_response(400, headers, json.dumps(body))
                return response

            client = datastore.Client()
            query = client.query(kind='user')
            result = query.add_filter('email', '=', email).fetch(1)

            user = [dict(e) for i, e in enumerate(result)]
            if user:
                if user[0]['question'] == question and user[0]['answer'] == answer:
                    body['message'] = 'User authenticated successfully!'
                    try:
                        cursor.execute(
                            f"INSERT INTO user_state (email, is_online) VALUES ('{email}', '{1}') ON DUPLICATE KEY UPDATE email='{email}', is_online='{1}';")
                        connection.commit()
                        connection.close()
                        response = make_response(
                            200, headers, json.dumps(body))
                        return response
                    except Exception as e:
                        body['error'] = str(e)
                        response = make_response(
                            500, headers, json.dumps(body))
                        return response
                body['error'] = 'Security question and answer do not match!'
                response = make_response(401, headers, json.dumps(body))
                return response

            body['error'] = 'User not found'
            response = make_response(404, headers, json.dumps(body))
            return response

        body['error'] = "Request missing parameters!"
        response = make_response(400, headers, json.dumps(body))
        return response

    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
