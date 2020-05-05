import os
import pyrebase
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from config import app_config 

# databse
db = SQLAlchemy()

# Init ma
ma = Marshmallow()

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

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    ma.init_app(app)
    return app