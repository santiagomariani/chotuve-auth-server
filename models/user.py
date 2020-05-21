from app import db, ma

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(50))
    image_location = db.Column(db.String(2083))
    admin = db.Column(db.Boolean)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'display_name', 'phone_number', 'image_location')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
