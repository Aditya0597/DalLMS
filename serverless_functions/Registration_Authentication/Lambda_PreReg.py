'''
    Author: Aditya Patel
    Python Version: 3.7
    Description: Handles user confirmation
'''
import json


def lambda_handler(event, context):
    event['response']['autoConfirmUser'] = True
    return event
