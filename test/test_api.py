import pytest
from test.conftest import *
from models.models import User

def test_simple_ping(db_handle, testapp):
    user = User(email="santiagomariani2@gmail.com",
                display_name="Santiago Mariani",
                phone_number="2254405503",
                image_location="http://www.google.com.ar",
                admin=False)
    db_handle.session.add(user)
    db_handle.session.commit()
    response = testapp.post('/reset-codes', json={'email':"santiagomariani2@gmail.com"})
    print(response.data)
    assert response.status_code == 200