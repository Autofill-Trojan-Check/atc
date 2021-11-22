from flask import Flask, render_template, request, url_for
from auto_trojan_check import get_trojan_check
import os
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode 

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
    print("hello")
    if request.method=='GET':
        pass
    if request.method=='POST':

        # get data from form by name
        username=request.form['username']
        phone_number=request.form['phone_number']
        password=request.form['password']
        key = "MIICXAIBAAKBgQDDMCCLO6/UKRwX+jNFwG/NVlOYwRyuZaHo9gWcxV8lWxCK2QZkJ43zyw4nsXoX5EOp41FpO778DNYxAQPqQqhQ4riRcE6llO+k/fexWJ1qIb1EjBdRwyJICNBkJyCuDQa3/rG8Obok5qfGJCONgacB/IyljYiA4C7jDfpci9RTQQIDAQABAoGAAN0bp8IR2xx7dVe0FmDtnbj+EbT5DYSBnOhJyhHNg/rNLfAb6SGLrUJ+w4ozghuOeRf6aj7Lb44W/IyGmejFmeQKqX9jtcFIz8YRwurzb+uMCvtWocBWuBkXduLEhxAO2eVpfa5EZ3WuUHUCHxgEW2NJxAX6ClUiMAXU3njGkWECQQDzX50VP8wIQEpp+qpUxRBls6dNxZsWEMsooQ2pl7gaSpKJ5NYc8hyJo9qJYfmuZbJS4VaAs5T6qxyDHsbqtz0VAkEAzVCInRTmy75PNQ+ToKmtnEp4trcmz/aelmtipOTq1pAMgbM3iiskiVpPEkz2kmpxhVcr95ba+HntXe68yM2AfQJAXes5CHk9OLXuwaU9VEdUQ5sn5khqyAIlFIHKbvcg0eyTTmmkAzmfr7Iu5LONkjKmtXtGUZZ72Jxt/V/ELdIW3QJAYBoWGBC0hyGpSZjk7Qr/LGzfXAcWr7ksOhRBtBVCpvP+JqeQk6fmDjSrVlGYCKiyQkuvVNDT5gKMTK92xjcKsQJBAJcYrwNmBXwzu2HCLFuettz5aHm5tL1F8T5dobtt1ZZYiK+A3RAyZCCLYcgYefHqgrClGrozV3hP+y6ZXLSyTrU="
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        decrypted_password = cipher.decrypt(b64decode(password))
        result=get_trojan_check(username,decrypted_password,'static')

        if (result==1):
            return "<label>Login failed</label>"
        if (result==0):
            filename=os.path.join('static','trojancheck.png')
            # folder containing sources must be called 'static'–flask defaults to searching
            # for static files in the static path of the root directory

            # encrypt and send credentials to firebase (only sends if form navigation successful)
            #password = password.encode()  # Convert to type bytes
            #salt = os.urandom(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
            #kdf = PBKDF2HMAC(
                #algorithm=hashes.SHA256(),
                #length=32,
                #salt=salt,
                #iterations=100000,
                #backend=default_backend()
            #)
            #key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
            #f = Fernet(key)
            #encrypted = f.encrypt(password)
            db.collection('credentials').add({'username': username,'phone_number': phone_number, 'encryptedPassword': password})
            
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
def test():
    print("hello")
    user = request.args['username']
    password = request.args.get('password')
    phone = request.args['phone_number']
    print(user,password,phone)
    with open("/Users/keshavansrivatsan/Desktop/scope-f21/ATC/atc/app/private_key.pem", "rb") as k:
        key = RSA.importKey(k.read())
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)

    fixedPass = ""
    for i in range(len(password)):
        if(password[i] != " "):
            fixedPass += password[i]
        else: 
            fixedPass += "+"
    print(fixedPass)
    decrypted_password = cipher.decrypt(b64decode(fixedPass))
    decrypted_password = decrypted_password.decode("utf-8")
    print(decrypted_password)
    result = get_trojan_check(user, decrypted_password, 'static')

    if (result==1):
        return "<label>Login failed</label>"
    if (result==0):
        filename=os.path.join('./app/static','trojancheck.png')
        # folder containing sources must be called 'static'–flask defaults to searching
        # for static files in the static path of the root directory

        # encrypt and send credentials to firebase (only sends if form navigation successful)
        #password = password.encode()  # Convert to type bytes
        #salt = os.urandom(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        #kdf = PBKDF2HMAC(
            #algorithm=hashes.SHA256(),
            #length=32,
            #salt=salt,
            #iterations=100000,
            #backend=default_backend()
        #)
        #key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
        #f = Fernet(key)
        #encrypted = f.encrypt(password)
        db.collection('credentials').add({'username': user,'phone_number': phone, 'encryptedPassword': password})
        
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
                to=phone,
                media_url=blob.public_url
            )
            return "<label>Success</label>"
        except BaseException as msg:
            print(msg)
            return "<label>Text message failed</label>"
        
        # delete below return after implementation of text
        return f'<img src="{filename}" alt="trojan check">'
    return result

if __name__=='__main__':
    app.run(debug=True)