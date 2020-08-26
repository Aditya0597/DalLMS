'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Gets the list of user files!
'''
import json
import pymysql


def make_response(statusCode, headers, body):
    response = {
        "statusCode": statusCode,
        "headers": headers,
        "body": body
    }
    return response


def getUserFiles(request):
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
            if ('email' not in data_keys) or ('file_name' not in data_keys) or ('is_upload' not in data_keys):
                body["error"] = "Request missing parameters!"
                response = make_response(400, headers, json.dumps(body))
                return response
            email = data['email']
            file_name = data['file_name']
            is_upload = data['is_upload']
            if is_upload:
                try:
                    cursor.execute(
                        f"SELECT * FROM user_reg where email='{email}';")
                    user = cursor.fetchall()
                    connection.commit()
                    email = user[0]['email']
                    name = user[0]['name']
                    gender = user[0]['gender']
                    institute = user[0]['institute']
                    role = user[0]['role']
                    cursor.execute(
                        f"INSERT INTO user_files (email, name, file_name, role, institute) VALUES ('{email}','{name}','{file_name}','{role}','{institute}');")
                    connection.commit()
                    connection.close()
                    body['result'] = user
                    response = make_response(200, headers, json.dumps(body))
                    return response
                except Exception as e:
                    body['error'] = str(e)
                    response = make_response(500, headers, json.dumps(body))
                    return response
            else:
                try:
                    cursor.execute(
                        f"SELECT * FROM user_files where email='{email}';")
                    user = cursor.fetchall()
                    connection.commit()
                    connection.close()
                    body['result'] = user
                    response = make_response(200, headers, json.dumps(body))
                    return response
                except Exception as e:
                    body['error'] = str(e)
                    response = make_response(500, headers, json.dumps(body))
                    return response

    except Exception as e:
        body['error'] = str(e)
        response = make_response(500, headers, json.dumps(body))
        return response
