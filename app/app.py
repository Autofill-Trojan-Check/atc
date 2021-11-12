from flask import Flask, render_template, request, url_for
from auto_trojan_check import get_trojan_check
import os

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
        password=request.form['password']
        result=get_trojan_check(username,password,'static')

        if (result==1):
            return "<label>Login failed</label>"
        if (result==0):
            filename=os.path.join('static','trojancheck.png')
            # folder containing sources must be called 'static'–flask defaults to searching
            # for static files in the static path of the root directory
            return f'<img src="{filename}" alt="trojan check">'
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)