import pyrebase

# Firebase configuration

config = {
    "apiKey": "AIzaSyDlBeowWP8UPWsvk9kXj9JDaN5_xsuNu4I",
    "authDomain": "chotuve-videos.firebaseapp.com",
    "databaseURL": "https://chotuve-videos.firebaseio.com",
    "projectId": "chotuve-videos",
    "storageBucket": "chotuve-videos.appspot.com",
    "messagingSenderId": "662757364228",
    "appId": "1:662757364228:web:02d934f2819b5d58581b51"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()