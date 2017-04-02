import os
from clarifai.rest import ClarifaiApp
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser, CurrentUser
import config
import bing_scraper as bs
import process_menu as pm
import requests

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "test_secret_key"
clarifai_descpt = {}

#urls = []

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/tmp/'
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
    session.clear()
    print session
    # Get the name of the uploaded file
    files = request.files.getlist('file[]')
    urls = []
    clarifai_app = ClarifaiApp(app_id='Lo1-3OPriyWss221gHySMX_ZdZFxer6nQe3BeQBz', app_secret='beN70gnQlx9oHiYwjqcFnlbhjStP63LlZaYUWQV7')
    for file in files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
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
    print request
    print request.form
    metadata["title"] = request.form["restaurantName"]
    metadata["people"] = request.form.getlist("people[]")
    location= request.form["location"]
    metadata["email_ids"] = request.form.getlist("emails[]")
    tod = request.form["tod"]
    menu = bs.getMenu(metadata["title"])
    metadata["amount"], metadata["priceDist"] = pm.process(menu, clarifai_descpt, tod)
    reply = metadata
    print reply, type(reply)
    names = reply['people']
    emails = reply['email_ids']
    session['title'] = reply['title']
    session['people'] = []
    session['amount'] = metadata['amount']
    session['priceDist'] = metadata['priceDist']
    for i in range(len(names)):
        session['people'].append({'name':names[i], 'email':emails[i]})
    print session
    return redirect('/split')

@app.route('/split')
def split_bill():

    # next 3 lines to be commented before deployment with UI   
    # session['title'] = 'TITLE'
    # session['people'] = [{'name':'Shreyas','email':'udupa_shreyas@yahoo.co.in'}, {'name':'Mridul','email':'g'}]
    # session['amount'] = '21.9'

    sObj = Splitwise(config.ckey, config.csecret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)

@app.route('/authorize')
def authorize():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    sObj = Splitwise(config.ckey, config.csecret)
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    session['access_token'] = access_token
    return redirect('/with_friends')

@app.route('/with_friends')
def usage():
    print session
    sObj = Splitwise(config.ckey,config.csecret)
    sObj.setAccessToken(session['access_token'])
    me = sObj.getCurrentUser()
    friends = sObj.getFriends()

    # add people in group to friends list on Splitwise
    friendnames = []

    for f in friends:
        friendnames.append(f['first_name'])

    tbanames = []
    tbaemails = []
    allnames = []
    for f in session['people']:
        allnames.append(f['name'])
        if f['name'] not in friendnames:
            tbanames.append(f['name'])
            tbaemails.append(f['email'])
    sObj.createFriends(tbanames,tbaemails)

    # create expense
    expense = Expense()
    expense.setCost(session['amount'])
    expense.setDescription(session['title'])

    friends = sObj.getFriends()

    # equal share
    total = float(session['amount'])
    num_people = len(session['people']) + 1
    share = total/num_people
    share = float("{0:.2f}".format(share))

    user1 = ExpenseUser()
    user1.setId(me.getId())
    user1.setPaidShare(str(total))
    if (share * num_people) < total:
        owed = share + (total - (share*num_people))
    else:
        owed = share
    user1.setOwedShare(str(owed))

    users = [user1]

    print allnames

    for f in friends:
        if f['first_name'] in allnames:
            print f['first_name']
            user1 = ExpenseUser()
            user1.setId(f['id'])
            user1.setPaidShare('0.00')
            user1.setOwedShare(str(total / num_people))
            users.append(user1)
    expense.setUsers(users)

    clarifai_descpt = {}

    try:
        expense = sObj.createExpense(expense)
        print expense.getId()
        return session
    except Exception, e:
        return 'error'

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=5000)