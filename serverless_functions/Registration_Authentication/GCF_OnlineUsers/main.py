'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Gets the list of online users!
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


def getOnline(request):
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
            if ('email' not in data_keys) or ('is_logout' not in data_keys):
                body["error"] = "Request missing parameters!"
                response = make_response(400, headers, json.dumps(body))
                return response
            email = data['email']
            is_logout = data['is_logout']
            if is_logout:
                try:
                    cursor.execute(
                        f"UPDATE user_state SET is_online = '{0}' WHERE email ='{email}';")
                    connection.commit()
                    connection.close()
                    body['message'] = "User offline!"
                    response = make_response(200, headers, json.dumps(body))
                    return response
                except Exception as e:
                    body['error'] = str(e)
                    response = make_response(500, headers, json.dumps(body))
                    return response
            else:
                try:
                    cursor.execute(
                        f"SELECT user_reg.name, user_reg.institute, user_reg.role, user_reg.email FROM user_state INNER JOIN user_reg ON user_state.email=user_reg.email WHERE is_online='{1}';")
                    online_users = cursor.fetchall()
                    result = {
                        'active_users': online_users
                    }
                    connection.commit()
                    connection.close()
                    body['result'] = result
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
