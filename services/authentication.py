from exceptions.exceptions import UserUnauthorizedError
import firebase_admin
import os
from firebase_admin import auth

class AuthenticationFirebase():

    def __init__(self):
        self.firebase_app = firebase_admin.initialize_app()
        self.auth = auth

    def verify_id_token(self, token):
        try:
            user_data = self.auth.verify_id_token(token)
        except self.auth.RevokedIdTokenError:
            raise UserUnauthorizedError(f"Token has been revoked.")
        except self.auth.ExpiredIdTokenError:
            raise UserUnauthorizedError(f"Token has expired.")
        except (self.auth.InvalidIdTokenError, ValueError):
            raise UserUnauthorizedError(f"Token is invalid.")
        return user_data

    def update_password(self, email, password):
        user_data = auth.get_user_by_email(email)
        uid = user_data.uid
        self.auth.update_user(uid, password=password)


class AuthenticationFake():

    def __init__(self):
        self.user_data = {'email': 'santiagomariani2@gmail.com', 'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'}
        
        self.expiredToken = False
        self.revokedToken = False
        self.invalidToken = False

    def verify_id_token(self, token):
        if self.revokedToken:
            raise UserUnauthorizedError(f"Token has been revoked.")
        if self.expiredToken:
            raise UserUnauthorizedError(f"Token has expired.")
        if self.invalidToken:
            raise UserUnauthorizedError(f"Token is invalid.")
        return self.user_data
    
    def update_password(self, email, password):
        return True

    def setExpiredToken(self):
        self.expiredToken = True

    def setRevokedToken(self):
        self.revokedToken = True
    
    def setInvalidToken(self):
        self.invalidToken = True

auth_service = AuthenticationFirebase() if os.environ['APP_SETTINGS'] != 'development' else AuthenticationFake()
