import pytest
from test.conftest import *
from models.models import User

"""
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
"""

token = 'WlxyCjKBDOfjJAbW800G57o4eBIpe3nJwTiPrJJgeTnTX0RPzc0XxZkG0y2QGkJOr9Pu3V8unfkp0xhFx9b802G3gPsJ150USj1T0C9Nvi1Gy4GRz3FyaBgPoPXg'

def test_register_user_success(testapp):
    """Register a user with a valid token and data"""
    response = testapp.post('/users', json={'email':'santiagomariani2@gmail.com',
                                            'display_name': 'Santiago Mariani',
                                            'phone_number': '2254405503',
                                            'image_location': 'http://www.google.coma.ar'}
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    assert json_data['message'] == 'ok'
    assert response.status_code == 200

def test_reset_code_success(testapp):
    """Get a reset code with a valid email (a user with that email exist)"""
    response = testapp.post('/reset-codes', json={'email': 'santiagomariani2@gmail.com'})
    json_data = response.get_json()
    assert json_data['message'] == 'ok'                                       
    assert response.status_code == 200