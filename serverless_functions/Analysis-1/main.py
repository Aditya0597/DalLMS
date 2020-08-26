import os
import tempfile
from werkzeug.utils import secure_filename
from google.cloud import storage
from flask import jsonify
import pickle
import csv
import json


bucket_name = 'upload-file-for-analysis'
file_to_write = 'Analyzed_data.txt'
client = storage.Client()
bucket = client.get_bucket(bucket_name)

def analyzeFile(request):
    request_json = request.get_json(silent=True)
    uploaded_file_name = request_json['name']
    print(uploaded_file_name)
    print(request_json)

    file_path = get_file_path(file_name)
     	download_file(file_name,file_path)
     	with open(file_path,'rb') as pickle_file:
        	model= pickle.load('model_training.pkl')

    file_path = get_file_path(file_name)
     	download_file(file_name,file_path)
     	with open(file_path,'rb') as pickle_file:
        	vectorizer= pickle.load('vectorizer_training_model.pkl')

    matrix = vectorizer.transform([uploaded_file_name])
    res = model.predict(matrix)
    print('Matrix: {}'.format(matrix))
    print('Prediction: {}'.format(res))
    centeroides = model.cluster_centers_[center_number]
    metadata = {
         'file_name': uploaded_file_name,
         'center_number': center_number,
         'centeroides': str(centeroides)
    }
    print('Metadata: {}'.format(metadata))
    blob = bucket.get_blob(file_to_write)
    print(blob)
    data = json.loads(blob.download_as_string(client=None))
    print(data)
    if not data:
          list = []
          list.append(metadata)
          print(list)
                   
    with tempfile.NamedTemporaryFile() as temp:
             blob.download_to_filename(temp.name)
    print(blob.download_to_filename(temp.name))
    blob.download_to_filename(file_to_write)
    with open(temp.name,'a') as f:
       f.write(metadata)
    blob = bucket.blob(file_to_write)
    blob.upload_from_filename(temp.name)


