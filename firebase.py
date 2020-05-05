import pyrebase

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