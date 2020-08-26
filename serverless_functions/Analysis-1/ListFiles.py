import os
from google.cloud import storage
from flask import jsonify

bucket_name = 'upload-file-for-analysis'
client = storage.Client()
bucket = client.get_bucket(bucket_name)

def listfiles(request):
    data = []
    blobs = client.list_blobs(bucket_name)
    print('Blobs:{}'.format(blobs))
    for blob in blobs:
         print(blob)
         print('Retrieve Blob Metadata:{}'.format(blob.metadata))
         blobData = [blob.name,blob.metadata]
         data.append(blobData)
         print('Appended Data:',data)
         # print('Blobdata',blobData)
         print('Json',jsonify(analysis=data))
    return jsonify(data)