import pymysql
import json

#Configuration Values
endpoint = 'serverless.cljjsiiqwmmz.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Test1234'
database_name = 'serverless'

#Connection
connection = pymysql.connect(endpoint, user=username,
	passwd=password, db=database_name)

def lambda_handler(event, context):
	cursor = connection.cursor()
	print("Request: " + str(event))
	
	org_input = event['currentIntent']['slots']['Organization']
	
	cursor.execute("SELECT name FROM user_reg WHERE institute='%s'" % org_input)

	rows = cursor.fetchall()
	users = ""
	for row in rows:
		users += str(row).replace(",","")

	print(users)
		
	response = {
		"dialogAction": {
			"type": "Close",
			"fulfillmentState": "Fulfilled",
			"message": {
				"contentType": "PlainText",
				"content": "All users in your organization are: " + users
			}
		}
	}
	return response