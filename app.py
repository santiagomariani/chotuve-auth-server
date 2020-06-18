import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from flask_failsafe import failsafe 
from flask_restful import Api
from flask_cors import CORS
from config import app_config

# database
db = SQLAlchemy()

# Init ma
ma = Marshmallow()

# Flask restful 
api = Api()

from resources import register_routes
from handlers import register_error_handlers

@failsafe
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    import logging
    logging.basicConfig(
        level=logging.getLevelName(app.config.get("LOG_LEVEL"))
    )

    logger = logging.getLogger("App")
    logger.info("Starting app!")

    register_routes(api)
    register_error_handlers(app)

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    return app