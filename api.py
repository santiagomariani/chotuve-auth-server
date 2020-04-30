import time
import os
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

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))

    def __init__(self, email):
        self.email = email

# Goal Schema

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    user = User(data['email'])
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return user_schema.jsonify(user)

@app.route('/', methods=['GET'])
def test():
    return 'hola como estas viejo'

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')