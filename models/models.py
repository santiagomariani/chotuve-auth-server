from app import db, ma
import logging

# User
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(50))
    image_location = db.Column(db.String(2083))
    admin = db.Column(db.Boolean)
    reset_code = db.relationship('ResetCode', backref='user', uselist=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'display_name', 'phone_number', 'image_location')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

import secrets
from services.time import time_service

# ResetCode
class ResetCode(db.Model):
    __tablename__ = "reset_code"

    _EXPIRATION_TIME_IN_MINUTES = 15

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=time_service.get_date())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)

    def __init__(self, user):
        # delete default
        self.timestamp = time_service.get_date()
        self.code = secrets.token_urlsafe(4)
        self.user = user

    def has_expired(self):
        logger = logging.getLogger(self.__class__.__name__)
        present_time = time_service.get_date()
        expiration_time = time_service.sum_minutes_to_date(self.timestamp, self._EXPIRATION_TIME_IN_MINUTES)
        logger.debug(f"present time: {present_time}")
        logger.debug(f"time to compare with: {expiration_time}")
        return present_time > expiration_time
