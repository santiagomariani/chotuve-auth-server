import time
import os

# flask
from flask import Flask, jsonify, request, session, redirect, url_for, make_response

# Init app
app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))

# Database

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set secret key
app.secret_key = b'\x0c{|7\x05\\t\xfe\xc8\x99\xc4r\xda\x82\xcd\x19\xf6\x18$\xca\xc2\xbc)\xe3'

@app.route('/prueba', methods=['GET'])
def test():
    result = {'message':'hola como estas'}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')