import time
import os
import pyrebase
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# flask
from flask import Flask, jsonify, request, session, redirect, url_for, make_response

# Init app
app = Flask(__name__)

app.config.from_object("config.Config")

# databse
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Set secret key
#app.secret_key = b'\x0c{|7\x05\\t\xfe\xc8\x99\xc4r\xda\x82\xcd\x19\xf6\x18$\xca\xc2\xbc)\xe3'

# Firebase configuration

config = {
    "apiKey": "AIzaSyBLnthSo8jqYrARFO2OPYAS1fNgqi9F5tE",
    "authDomain": "chotuve-auth-744e0.firebaseapp.com",
    "databaseURL": "https://chotuve-auth-744e0.firebaseio.com",
    "projectId": "chotuve-auth-744e0",
    "storageBucket": "chotuve-auth-744e0.appspot.com",
    "messagingSenderId": "110559197092",
    "appId": "1:110559197092:web:464eea40204a2de3d8f331",
    "measurementId": "G-2NT9H1XZVG"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')