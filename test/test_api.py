import pytest
from test.conftest import *
from models.models import User, ResetCode
from services.authentication import auth_service

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

def test_register_user_with_expired_token(testapp):
    """Register a user with a expired token"""
    auth_service.setExpiredToken()
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    
    auth_service.setValidToken()
    
    assert json_data['message'] == 'Token has expired.'
    assert response.status_code == 401
    

def test_register_user_with_invalid_token(testapp):
    """Register a user with a invalid token"""
    auth_service.setInvalidToken()
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    
    auth_service.setValidToken()
    
    assert json_data['message'] == 'Token is invalid.'
    assert response.status_code == 401

def test_register_user_with_revoked_token(testapp):
    """Register a user with a revoked token"""
    
    auth_service.setRevokedToken()
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    
    auth_service.setValidToken()
    
    assert json_data['message'] == 'Token has been revoked.'
    assert response.status_code == 401

def test_register_user_without_token(testapp):
    """Register a user without token"""
    response = testapp.post('/users', json=user_data)

    json_data = response.get_json()
    
    assert json_data['message'] == 'Missing user token!'
    assert response.status_code == 401

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

    testapp.put('/users/1', json=user_data
                                    , headers={'x-access-token': token}) 

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

# POST /change-password-with-reset-code

def test_change_password_with_reset_code(testapp):
    """Should change the password with a valid reset code"""
    # I use the reset code created before.
    code = ResetCode.query.filter_by(id=1).first().code
    response = testapp.post('/change-password-with-reset-code',
                            json={'code':code,'password':'un_password','email':'santiagomariani2@gmail.com'})
    json_data = response.get_json()
    assert json_data['message'] == 'ok'
    assert response.status_code == 200 

# GET /users?name=some_name&phone=some_phone&email=some_email

def test_get_users_data_filtered_by_display_name(testapp):
    """Should return users data filtered by display name 
    (users which names contains indicated display name)"""
    
    user_a = User(email='armandoestabanquito@gmail.com',
                    display_name='Armando Estaban Quito',
                    phone_number='11533223536',
                    image_location='http://www.google.com.ar',
                    admin=False)
    user_b = User(email='armando2020@gmail.com',
                    display_name='Martin Armando Quito',
                    phone_number='12121555530',
                    image_location='http://www.facebook.com',
                    admin=False)
    user_c = User(email='carlosgutierrez@gmail.com',
                    display_name='Carlos Gutierrez',
                    phone_number='1125553512',
                    image_location='http://www.youtube.com',
                    admin=False)
    db.session.add(user_a)
    db.session.add(user_b)
    db.session.add(user_c)
    db.session.commit()

    response = testapp.get('/users?name=Armando', headers={'x-access-token': token})
    json_data = response.get_json()
    
    assert len(json_data['users']) == 2

    for user in json_data['users']:
        assert ('Armando' in user['display_name'])

    assert response.status_code == 200 

def test_get_users_data_filtered_by_phone_number(testapp):
    """Should return users data filtered by phone number"""
    response = testapp.get(f"/users?phone={user_data['phone_number']}", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 1

    assert json_data['users'][0]['display_name'] == user_data['display_name']
    assert response.status_code == 200

def test_get_users_data_filtered_by_email(testapp):
    """Should return users data filtered by email"""
    response = testapp.get(f"/users?email={user_data['email']}", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 1

    assert json_data['users'][0]['display_name'] == user_data['display_name']
    assert response.status_code == 200