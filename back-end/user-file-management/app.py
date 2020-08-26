import logging
import os
import tempfile

from flask import Flask, request, jsonify, send_file, make_response
from google.cloud import storage

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure this environment variable
CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET_USER')
# Configure this environment variable
CLOUD_STORAGE_BUCKET_CHAT = os.environ.get('CLOUD_STORAGE_BUCKET_CHAT')

headers = {'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
           'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*', 'Access-Control-Max-Age': '3600'}


@app.route('/')
def index():
    return """
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file"> <br>
    <input type="submit">
</form>
"""


@app.route('/file/user', methods=['GET'])
def download_user_file():

    file_name = request.args.get('name')

    if not file_name:
        return jsonify(message="Filename cannot be empty"), 409

    try:
        gcp_storage = storage.Client()

        bucket = gcp_storage.bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile() as temp:
            blob.download_to_filename(temp.name)
            return send_file(temp.name, attachment_filename=file_name, as_attachment=True), headers

    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while downloading the file", error=str(e)), 409


@app.route('/file/chat', methods=['GET'])
def download_chat_file():

    file_name = request.args.get('name')

    if not file_name:
        return jsonify(message="Filename cannot be empty"), 409

    try:
        gcp_storage = storage.Client()

        bucket = gcp_storage.bucket(CLOUD_STORAGE_BUCKET_CHAT)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile() as temp:
            blob.download_to_filename(temp.name)

            return send_file(temp.name, attachment_filename=file_name, as_attachment=True), headers

    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while downloading the file", error=str(e)), 409, headers


@app.route('/file/user', methods=['GET'])
def download_blob():

    file_name = request.args.get('name')

    if not file_name:
        return jsonify(message="Filename cannot be empty"), 409

    try:
        gcp_storage = storage.Client()

        bucket = gcp_storage.bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile() as temp:
            blob.download_to_filename(temp.name)
            return send_file(temp.name, attachment_filename=file_name, as_attachment=True)

    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while downloading the file", error=str(e)), 409,headers


@app.route('/files/user', methods=['GET'])
def get_all_files():
    try:
        # Initializing GCP storage client
        gcp_storage = storage.Client()

        # Fetching the blobs object for the desired bucket
        blobs = gcp_storage.list_blobs(CLOUD_STORAGE_BUCKET)

        files = []
        for blob in blobs:
            files.append(blob.name)

        app.logger.info("Files retrieved from the bucket: {} are: {}".format(CLOUD_STORAGE_BUCKET, files))
        return jsonify(files=files), 200, headers

    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while uploading the file", error=str(e)), 409, headers


@app.route('/files/chat', methods=['GET'])
def get_chat_files():
    try:
        # Initializing GCP storage client
        gcp_storage = storage.Client()

        # Fetching the blobs object for the desired bucket
        blobs = gcp_storage.list_blobs(CLOUD_STORAGE_BUCKET_CHAT)

        files = []
        for blob in blobs:
            files.append(blob.name)

        app.logger.info("Chat files retrieved from the bucket: {} are: {}".format(CLOUD_STORAGE_BUCKET_CHAT, files))
        return jsonify(files=files), 200, headers

    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while uploading the file", error=str(e)), 409, headers


@app.route('/upload', methods=['POST'])
def upload_file():
    selected_file = request.files.get('file')

    print(selected_file.filename)

    if not selected_file:
        return jsonify(error='No file selected for upload.'), 400

    app.logger.info("File selected for upload {}".format(selected_file.filename))

    try:
        # Initializing GCP storage client
        gcp_storage = storage.Client()

        # Getting the bucket URL where the file needs to be uploaded
        bucket = gcp_storage.get_bucket(CLOUD_STORAGE_BUCKET)

        # Initializing blob object
        blob = bucket.blob(selected_file.filename)

        # Uploading the file
        blob.upload_from_string(
            selected_file.read(),
            content_type=selected_file.content_type
        )

        res = "File: {} has been successfully uploaded to the bucket {}".format(selected_file.filename
                                                                                , CLOUD_STORAGE_BUCKET)
        app.logger.info(res)
        return jsonify(message="File has been successfully uploaded", filename=selected_file.filename), 201 , headers
    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An error occurred while uploading the file", error=str(e)), 409, headers


@app.errorhandler(500)
def server_error(e):
    app.logger.error('An error occurred during a request.')
    return jsonify(message="An internal error occurred", error="{} See logs for full stacktrace.".format(e)) \
        , 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
