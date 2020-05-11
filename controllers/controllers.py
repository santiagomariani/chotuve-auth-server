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
    image_location = data['image_location']

    #create user in firebase
    auth.create_user_with_email_and_password(email, password)

    #create user in my database
    user = User(email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        image_location=image_location)

    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.json
    
    email = data['email']
    password = data['password']
    
    #create user in firebase
    user = auth.sign_in_with_email_and_password(email, password)
    token = user['idToken']
    return jsonify({'user-token': token})

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return 'hola'

@app.route('/', methods=['GET'])
def hello():
    return "hola flaco!"
