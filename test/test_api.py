import pytest
from test.conftest import *
from models.models import User

token = 'WlxyCjKBDOfjJAbW800G57o4eBIpe3nJwTiPrJJgeTnTX0RPzc0XxZkG0y2QGkJOr9Pu3V8unfkp0xhFx9b802G3gPsJ150USj1T0C9Nvi1Gy4GRz3FyaBgPoPXg'
user_data = {'email':'santiagomariani2@gmail.com',
            'display_name': 'Santiago Mariani',
            'phone_number': '2267458826',
            'image_location': 'http://www.google.com.ar'}
# POST /users

def test_register_user(testapp):
    """Register a user with a valid token and data."""
    # This test creates a user that is used in the other tests.
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    assert json_data['message'] == 'ok'
    assert response.status_code == 200

# GET /users/<int:id>

def test_get_user_data_with_id(testapp):
    """Should return user data if user id and token is valid."""
    response = testapp.get('/users/1', headers={'x-access-token': token})
    json_data = response.get_json()
    
    result_data = user_data.copy()
    result_data["id"] = 1
    
    assert json_data == result_data
    assert response.status_code == 200

def test_get_user_data_of_user_that_does_not_exist(testapp):
    """Get the user data of a user that does not exist in db."""
    response = testapp.get('/users/2', headers={'x-access-token': token})
    json_data = response.get_json()

    assert json_data['message'] == 'No user found with ID: 2'
    assert response.status_code == 404  

# PUT /users/<int:id>

def test_modify_user_data_with_id(testapp):
    """Should modify user data if user id and token is valid."""
    
    new_data = {'email':'santiagomariani2@gmail.com',
                'display_name': 'Santiago Tomas Mariani',
                'phone_number': '2254444444',
                'image_location': 'http://www.facebook.com'}
    
    response = testapp.put('/users/1', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()
    
    assert json_data['message'] == 'ok'
    assert response.status_code == 200

    # check if data has changed

    response = testapp.get('/users/1', headers={'x-access-token': token})
    json_data = response.get_json()
    new_data["id"] = 1
    assert json_data == new_data

# POST /reset-codes

def test_reset_code(testapp):
    """Get a reset code with a valid email (a user with that email exist)."""
    response = testapp.post('/reset-codes', json={'email': 'santiagomariani2@gmail.com'})
    json_data = response.get_json()
    assert json_data['message'] == 'ok'                                       
    assert response.status_code == 200

# GET /users/id

def test_get_uid_from_token(testapp):
    """Should return uid just sending the token."""
    response = testapp.get('/users/id',
                            headers={'x-access-token': token})
    json_data = response.get_json()
    assert json_data['uid'] == 1
    assert response.status_code == 200    

