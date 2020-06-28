from exceptions.exceptions import UserUnauthorizedError
import firebase_admin
import os
from firebase_admin import auth

class AuthenticationFirebase():

    def __init__(self):
        self.firebase_app = firebase_admin.initialize_app()

    def verify_id_token(self, token):
        try:
            user_data = auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            raise UserUnauthorizedError(f"Token has been revoked.")
        except auth.ExpiredIdTokenError:
            raise UserUnauthorizedError(f"Token has expired.")
        except (auth.InvalidIdTokenError, ValueError):
            raise UserUnauthorizedError(f"Token is invalid.")
        return user_data

    def update_password(self, email, password):
        uid = self._get_uid_with_email(email)
        auth.update_user(uid, password=password)

    def update_email(self, old_email, new_email):
        uid = self._get_uid_with_email(old_email)
        auth.update_user(uid, email=new_email)
    
    def has_email_provider(self, email):
        user = auth.get_user_by_email(email)
        return user.provider_id == 'firebase' # check for a better way of doing this!

    def delete_user(self, email):
        uid = self._get_uid_with_email(email)
        auth.delete_user(uid)

    def create_user(self, email, password):
        auth.create_user(email=email, password=password)

    def _get_uid_with_email(self, email):
        user_data = auth.get_user_by_email(email)
        uid = user_data.uid
        return uid
    


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

    def update_email(self, old_email, new_email):
        return True
    
    def has_email_provider(self, email):
        return True

    def setExpiredToken(self):
        self.expiredToken = True
        self.revokedToken = False
        self.invalidToken = False

    def setRevokedToken(self):
        self.revokedToken = True
        self.expiredToken = False
        self.invalidToken = False
    
    def setInvalidToken(self):
        self.invalidToken = True
        self.expiredToken = False
        self.revokedToken = False

    def setValidToken(self):
        self.invalidToken = False
        self.expiredToken = False
        self.revokedToken = False

    def setData(self, data):
        self.user_data = data

    def delete_user(self, email):
        return True

    def create_user(self, email, password):
        return True

auth_service = AuthenticationFirebase() if os.environ['APP_SETTINGS'] != 'testing' else AuthenticationFake()
