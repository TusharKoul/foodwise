import os
from clarifai.rest import ClarifaiApp
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from splitwise import Splitwise
import config
import bing_scraper as bs
import process_menu as pm
import requests
import json

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "test_secret_key"
clarifai_descpt = {}

#urls = []

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/Users/swathi/photos/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return "Hello"


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    files = request.files.getlist('file[]')
    urls = []
    clarifai_app = ClarifaiApp()
    for file in files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            print(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            fname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fname)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            urls.append(fname)
        #print urls
    for image_url in urls:
        output = clarifai_app.tag_files([image_url], model='food-items-v1.0')
        guesses = [op["name"] for op in sorted(output['outputs'][0]['data']['concepts'], key=lambda x: x["value"], reverse=True)][:10]
        clarifai_descpt[image_url] = guesses
    return "Uploaded"

@app.route("/metadata", methods=["POST"])
def metadata():
    metadata = {}
    metadata["title"] = request.form["restaurantName"]
    metadata["people"] = request.form["people"].split(", ")
    location= request.form["location"]
    metadata["email_ids"] = request.form["emails"].split(",")
    tod = request.form["tod"]
    menu = bs.getMenu(metadata["title"])
    metadata["amount"] = pm.process(menu, clarifai_descpt, tod)
    print(metadata)
    requests.post("http://localhost:5000/split", data=json.dumps(metadata))
    return "Done"

@app.route("/split", methods=["POST"])
def split():
    print("In split")
    return "Done"

if __name__ == '__main__':
    app.run()
