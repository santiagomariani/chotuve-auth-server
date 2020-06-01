from app import db, ma
from datetime import datetime, timedelta
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

# ResetCode
class ResetCode(db.Model):
    __tablename__ = "reset_code"

    EXPIRATION_TIME_IN_MINUTES = 15

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)

    def has_expired(self):
        logger = logging.getLogger(self.__class__.__name__)
        present_time = datetime.utcnow()
        expiration_time = (self.timestamp + timedelta(minutes=self.EXPIRATION_TIME_IN_MINUTES))
        logger.debug(f"present time: {present_time}")
        logger.debug(f"time to compare with: {expiration_time}")
        return present_time > expiration_time