from app import db, ma

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))

    def __init__(self, email, first_name, last_name, phone_number):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number')

user_schema = UserSchema()
users_schema = UserSchema(many=True)