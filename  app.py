from flask import Flask
app = Flask(__name__)
#First, we need to define the starting point, also known as the root.
# #forward slash, his denotes that we want to put our data at the root of our routes.
@app.route('/')
def hello_world():
    return 'Hello world'
    
export FLASK_APP=app.py
Flask run