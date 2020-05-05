from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from models.user import User, user_schema
from app import db
from run import app
from firebase import auth

@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json
    
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']

    #create user in firebase
    auth.create_user_with_email_and_password(email, password)

    #create user in my database
    user = User(data['email'],
        data['first_name'],
        data['last_name'],
        data['phone_number'])

    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/', methods=['GET'])
def hello():
    return "hola flaco!"