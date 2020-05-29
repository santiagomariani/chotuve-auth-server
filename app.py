import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from config import app_config
from flask_failsafe import failsafe 
 
# databse
db = SQLAlchemy()

# Init ma
ma = Marshmallow()

@failsafe
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['BUNDLE_ERRORS'] = True


    db.init_app(app)
    ma.init_app(app)

    return app