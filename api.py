import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename

from splitwise import Splitwise
import config

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "test_secret_key"
urls = []

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/home/foodwise/photos/'
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
    #urls = []
    for file in files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            print filename
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            urls.append(url_for('uploaded_file',
                                filename=filename))
    return "Uploaded"

# Route that will handle splitwise account of user
@app.route('/split')
def split_bill():
    # secret key from config file
    sObj = Splitwise(config.ckey, config.csecret)
    # authorization URL to redirect to
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)

@app.route('/authorize')
def authorize():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    sObj = Splitwise(config.ckey, config.csecret)
    # get access to user account to make changes
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    # TODO
    return "Done"

if __name__ == '__main__':
    app.run()
