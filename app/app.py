from flask import Flask, render_template, request, url_for
from auto_trojan_check import get_trojan_check
import os

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
cred = credentials.Certificate("key.json")
# initialize with credentials and declare storage path
firebase_admin.initialize_app(cred,{'storageBucket':'autotrojancheck-ff14c.appspot.com'})

from twilio.rest import Client
# setup client
account_sid = 'AC2c5a7f1b45c89150eaa495eaea8b3f69' 
auth_token = '89b59d7ea4444326dff1a66f6a9f6b86'
client = Client(account_sid, auth_token)

db=firestore.client()

# create app; __name__ indicates the application's module–where to look for resources
app=Flask(__name__)

# registers the following function with the url "/"
# looks for html files in ./folder template (./ = current directory)
# GET is a method to retrieve data from the server
# POST is a method to send HTML data to the server
# ^^these are handlers for HTTP requests–data communication on the internet
@app.route("/",methods=['GET','POST'])
def index():
    # if GET or POST
    if request.method=='GET':
        pass
    if request.method=='POST':

        # get data from form by name
        username=request.form['username']
        phone_number=request.form['phone_number']
        password=request.form['password']
        result=get_trojan_check(username,password,'static')

        if (result==1):
            return "<label>Login failed</label>"
        if (result==0):
            filename=os.path.join('static','trojancheck.png')
            # folder containing sources must be called 'static'–flask defaults to searching
            # for static files in the static path of the root directory

            # encrypt and send credentials to firebase (only sends if form navigation successful)
            password = password.encode()  # Convert to type bytes
            salt = os.urandom(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
            f = Fernet(key)
            encrypted = f.encrypt(password)
            db.collection('credentials').add({'username': username,'phone_number': phone_number, 'encryptedPassword': encrypted})
            
            # upload image to firebase
            bucket=storage.bucket()
            blob=bucket.blob(filename)
            blob.upload_from_filename(filename)
            # make public
            blob.make_public()

            # text image to user
            try:
                message = client.messages.create(
                    body='auto trojan check',
                    from_='3108536936',
                    to=phone_number,
                    media_url=blob.public_url
                )
                return "<label>Success</label>"
            except BaseException as msg:
                print(msg)
                return "<label>Text message failed</label>"
            
            # delete below return after implementation of text
            return f'<img src="{filename}" alt="trojan check">'

    return render_template('index.html')


@app.route("/test",methods=['GET'])
def index():
    user = request.args['username']
    password = request.args['password']
    phone = request.args['phone_number']
    print(user,password,phone)
    result = get_trojan_check(user, password,'static')


    return  result

if __name__=='__main__':
    app.run(debug=True)