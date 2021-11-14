from flask import Flask, render_template, request, url_for
from auto_trojan_check import get_trojan_check
import os

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
    if request.method=='GET':
        pass
    if request.method=='POST':

        # get data from form by name
        username=request.form['username']
        phone_number=request.form['phone_number']
        password=request.form['password']
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n\
        MIICXAIBAAKBgQDJafuPdcMxZQyRWN3xnBj2KfUt7atj8TB5CGZ4r2OK7xZGY3BM\n\
        wKlyIhO49dL7/zWGFfsf751vlFIPMuF/iyd8zSfZiZzsuax0+kdw24FAXPDpevyq\n\
        Xyig2zNovaMmxnsHSHTDvk47gSf6SOU8PzFD7fKBkg3ACTuVIGHVMTm08QIDAQAB\n\
        AoGAB7EAZkNnp3nlt6Hed9zaJyxbAdyoRYdvA8WKWY7OYlPW/0Efh2QkFF5bb8i+\n\
        Edl2ax8Tw+3Gjqg/VKKWHI9tJomPvkxvXq37Utp5cM0j+W9E9bPCQESLGq/fQyOa\n\
        BQn1QMHOLtBKnaJ/Z/2OEpH2lkLL9ifij4HMz6cVhJuvIfECQQDb8+KQ9BrdgjTc\n\
        gzojuTx5pQGJIzvekN6wOdOLliPfBNPqFHpxxxDm1cN7/S7vWVBoD/ZI8Xc5gr7m\n\
        EQrN3FbnAkEA6mxOpoUKUp4YPlVEo2FTEfgQg8oEYSbFi79PWEHdQ2zr3IHGP/hx\n\
        rvIUMisBcUbPyMKrFGQ5FwUzqgisQoWSZwJAO4/Qk7Y2rDM9Q1WZ4eCgesRvJQbQ\n\
        iJWsaAZQveT7c8In7KR8/+CLOCc814+ZLSF/f56K7/fLdFxue3iz90kqkwJBAJtX\n\
        /GKixO1ssHoV/S8bXnYI4cDDjVVn4P6zXvwIYXy94Cq2oM5hb8xTxQhdsU4Ec8sB\n\
        HWec5qwXmV3y81v9sb8CQEvMCeYk/GI+Sc0ALWh00V3iJfNhSKL3Gs5vrXG6yp1O\n\
        gByKXnCmyMLB1DVEiiciRwUwHZ+kgjzI0tr9Nl/A7iY=\n\
        -----END RSA PRIVATE KEY-----"
        key = RSA.importKey(private_key)
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
    user = request.args['username']
    password = request.args['password']
    phone = request.args['phone_number']
    print(user,password,phone)
    private_key = "-----BEGIN RSA PRIVATE KEY-----\n\
    MIICXAIBAAKBgQDJafuPdcMxZQyRWN3xnBj2KfUt7atj8TB5CGZ4r2OK7xZGY3BM\n\
    wKlyIhO49dL7/zWGFfsf751vlFIPMuF/iyd8zSfZiZzsuax0+kdw24FAXPDpevyq\n\
    Xyig2zNovaMmxnsHSHTDvk47gSf6SOU8PzFD7fKBkg3ACTuVIGHVMTm08QIDAQAB\n\
    AoGAB7EAZkNnp3nlt6Hed9zaJyxbAdyoRYdvA8WKWY7OYlPW/0Efh2QkFF5bb8i+\n\
    Edl2ax8Tw+3Gjqg/VKKWHI9tJomPvkxvXq37Utp5cM0j+W9E9bPCQESLGq/fQyOa\n\
    BQn1QMHOLtBKnaJ/Z/2OEpH2lkLL9ifij4HMz6cVhJuvIfECQQDb8+KQ9BrdgjTc\n\
    gzojuTx5pQGJIzvekN6wOdOLliPfBNPqFHpxxxDm1cN7/S7vWVBoD/ZI8Xc5gr7m\n\
    EQrN3FbnAkEA6mxOpoUKUp4YPlVEo2FTEfgQg8oEYSbFi79PWEHdQ2zr3IHGP/hx\n\
    rvIUMisBcUbPyMKrFGQ5FwUzqgisQoWSZwJAO4/Qk7Y2rDM9Q1WZ4eCgesRvJQbQ\n\
    iJWsaAZQveT7c8In7KR8/+CLOCc814+ZLSF/f56K7/fLdFxue3iz90kqkwJBAJtX\n\
    /GKixO1ssHoV/S8bXnYI4cDDjVVn4P6zXvwIYXy94Cq2oM5hb8xTxQhdsU4Ec8sB\n\
    HWec5qwXmV3y81v9sb8CQEvMCeYk/GI+Sc0ALWh00V3iJfNhSKL3Gs5vrXG6yp1O\n\
    gByKXnCmyMLB1DVEiiciRwUwHZ+kgjzI0tr9Nl/A7iY=\n\
    -----END RSA PRIVATE KEY-----"
    key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    decrypted_password = cipher.decrypt(b64decode(password))
    result = get_trojan_check(user, decrypted_password, 'static')

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