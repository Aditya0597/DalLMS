import json
import boto3
import os

source_bucket = 'lms-chat-data'

def lambda_handler(event, context):
    
    print('triggering tweetPostProcessor function ')

    s3 = boto3.client("s3")
    comprehend = boto3.client('comprehend')
    
    json_res = []
    
    chat_session_list = s3.list_objects(Bucket=source_bucket)
    
    print(chat_session_list)
    
    if 'Contents' not in chat_session_list:
        response = {
            "statusCode": 404,
            "error": "No chat sessions found"
        }
        
        return json.dumps(response)
    
    for key in chat_session_list['Contents']:
        print(key['Key'])
        
        file_name = key['Key']
        
        fileData  = s3.get_object(Bucket= source_bucket, Key = file_name)
        content = fileData["Body"].read().decode('utf-8')
        
        chat_data_json = json.loads(content)
        print(chat_data_json)
        
        response = comprehend.detect_sentiment(Text = content, LanguageCode = 'en')
        print(response)
        
        chat_data_json["sentiment_analysis"] = response
        print('updated_json')
        print(chat_data_json)
        
        json_res.append(chat_data_json)
            
    return json.dumps(json_res)
    
