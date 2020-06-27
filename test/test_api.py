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

    result_data = user_data.copy()
    result_data["id"] = 1
    
    assert json_data == result_data
    assert response.status_code == 201

def test_register_user_with_expired_token(testapp):
    """Register a user with a expired token."""
    auth_service.setExpiredToken()
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    
    auth_service.setValidToken()
    
    assert json_data['message'] == 'Token has expired.'
    assert response.status_code == 401
    

def test_register_user_with_invalid_token(testapp):
    """Register a user with a invalid token."""
    auth_service.setInvalidToken()
    response = testapp.post('/users', json=user_data
                                    , headers={'x-access-token': token})
    json_data = response.get_json()
    
    auth_service.setValidToken()
    
    assert json_data['message'] == 'Token is invalid.'
    assert response.status_code == 401

def test_register_user_with_revoked_token(testapp):
    """Register a user with a revoked token."""
    
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
    
    assert json_data['message']['x-access-token'] == "Missing user's token."
    assert response.status_code == 400

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
    
    new_data["id"] = 1
    assert json_data == new_data
    assert response.status_code == 200

    testapp.put('/users/1', json=user_data
                                    , headers={'x-access-token': token})


def test_modify_display_name_with_id(testapp):
    """Should modify display name if id and token is valid."""

    new_data = {'display_name':'Jorge Fernandez'}
    
    response = testapp.put('/users/1', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()
    
    assert json_data['display_name'] == new_data['display_name']
    assert response.status_code == 200

    testapp.put('/users/1', json=user_data
                                    , headers={'x-access-token': token})

def test_modify_phone_number_with_id(testapp):
    """Should modify phone number if id and token is valid."""

    new_data = {'phone_number': '12345678910'}
    
    response = testapp.put('/users/1', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()
    
    assert json_data['phone_number'] == new_data['phone_number']
    assert response.status_code == 200

    testapp.put('/users/1', json=user_data
                                    , headers={'x-access-token': token})

def test_modify_image_location_with_id(testapp):
    """Should modify image location if id and token is valid."""

    new_data = {'image_location': 'http://www.heroku.com/some_image.jpeg'}
    
    response = testapp.put('/users/1', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()
    
    assert json_data['image_location'] == new_data['image_location']
    assert response.status_code == 200

    testapp.put('/users/1', json=user_data
                                    , headers={'x-access-token': token})

def test_cannot_modify_others_users_data_if_im_not_an_admin(testapp):
    """Should return a message saying I cant modify others users data if I am not an admin."""

    new_data = {'display_name': 'Jorge Fernandez'}
    
    response = testapp.put('/users/2', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()
    
    assert json_data['message'] == "Only admins can change others users data."
    assert response.status_code == 401

def test_modify_non_existing_user(testapp, db_handle):
    """Should return a message saying user does not exist."""
    new_data = {'display_name': 'Jorge Fernandez'}

    user = User.query.filter_by(id=1).first()
    user.admin = True

    db_handle.session.commit()
    
    response = testapp.put('/users/2', json=new_data
                                    , headers={'x-access-token': token}) 
    json_data = response.get_json()

    assert json_data['message'] == "No user found with ID: 2."
    assert response.status_code == 404


def test_modify_data_of_other_user_with_admin_user(testapp, db_handle):
    """Should be able to modify others users data with admin user."""
    new_data = {'display_name': 'Isidoro Tomas Gonzalez'}

    new_user = User(email='isodorogonzalez@gmail.com',
                    display_name='Isidoro Gonzalez',
                    phone_number='11533223536',
                    image_location='http://www.google.com.ar',
                    admin=False)
                
    db_handle.session.add(new_user)
    db_handle.session.commit()
    
    response = testapp.put(f"/users/{new_user.id}", json=new_data
                                    , headers={'x-access-token': token}) 

    json_data = response.get_json()

    assert json_data['display_name'] == new_data['display_name']
    assert response.status_code == 200


# POST /reset-codes

from services.time import time_service
from datetime import datetime

def test_get_reset_code(testapp):
    """Get a reset code with a valid email."""

    test_date = datetime(year=2020,month=6,day=5,minute=0,second=0)

    time_service.set_date(test_date)

    response = testapp.post('/reset-codes', json={'email': 'santiagomariani2@gmail.com'})

    json_data = response.get_json()

    assert json_data['message'] == 'ok'                                       
    assert response.status_code == 200
    assert ResetCode.query.count() == 1

def test_get_reset_code_with_invalid_email(testapp):
    """Should not be able to get reset code with invalid email (user does not exist)"""
    response = testapp.post('/reset-codes', json={'email': 'martinperez@gmail.com'})

    json_data = response.get_json()

    assert json_data['message'] == 'No user found.'                                       
    assert response.status_code == 404                                       

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

    test_date = datetime(year=2020,month=6,day=5,minute=14,second=0)
    time_service.set_date(test_date)

    response = testapp.post('/change-password-with-reset-code',
                            json={'code':code,'password':'un_password','email':'santiagomariani2@gmail.com'})
    
    json_data = response.get_json()
    
    assert json_data['message'] == 'ok'
    assert response.status_code == 200
    assert ResetCode.query.count() == 0 
    

def test_change_password_with_reset_code_when_code_is_expired(testapp):
    """Should not be able to change the password with a expired reset code"""
    # I use the reset code created before.

    test_date = datetime(year=2020,month=6,day=5,minute=0,second=0)
    time_service.set_date(test_date)

    testapp.post('/reset-codes', json={'email': 'santiagomariani2@gmail.com'})

    code = ResetCode.query.filter_by(id=1).first().code

    test_date = datetime(year=2020,month=6,day=5,minute=15,second=1)
    time_service.set_date(test_date)

    response = testapp.post('/change-password-with-reset-code',
                            json={'code':code,'password':'un_password','email':'santiagomariani2@gmail.com'})
    
    json_data = response.get_json()
    
    assert json_data['message'] == 'Reset code has expired.'
    assert response.status_code == 401
    assert ResetCode.query.count() == 1  

def test_change_password_with_reset_code_with_valid_reset_code_but_wrong_email(testapp):
    """Should not be able to change the password"""
    
    code = ResetCode.query.filter_by(id=1).first().code

    test_date = datetime(year=2020,month=6,day=5,minute=10,second=0)
    time_service.set_date(test_date)

    response = testapp.post('/change-password-with-reset-code',
                            json={'code':code,'password':'un_password','email':'jorgemendez@gmail.com'})
    json_data = response.get_json()

    assert json_data['message'] == 'Reset code is invalid.'
    assert response.status_code == 401
    assert ResetCode.query.count() == 1  

def test_change_password_with_invalid_reset_code(testapp):
    """Should not be able to change the password"""
    response = testapp.post('/change-password-with-reset-code',
                            json={'code':'534saX','password':'un_password','email':'santiagomariani2@gmail.com'})
    json_data = response.get_json()

    assert json_data['message'] == 'Reset code is invalid.'
    assert response.status_code == 401  

# GET /users?name=some_name&phone=some_phone&email=some_email

def test_get_users_data_filtered_by_display_name(testapp, db_handle):
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
    db_handle.session.add(user_a)
    db_handle.session.add(user_b)
    db_handle.session.add(user_c)
    db_handle.session.commit()

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

def test_get_users_per_page(testapp, db_handle):
    User.query.delete()
    db_handle.session.commit()

    an_email = "a@gmail.com"
    for i in range(0,12):  
        user_a = User(email=an_email,
                    display_name='Armando Estaban Quito',
                    phone_number='11533223536',
                    image_location='http://www.google.com.ar',
                    admin=False)

        db_handle.session.add(user_a)
        db_handle.session.commit()
        an_email = "a" + an_email
    
    response = testapp.get(f"/users?per_page=6&page=1", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 6
    assert json_data['page'] == 1
    assert json_data['total'] == 12

    response = testapp.get(f"/users?per_page=6&page=2", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 6
    assert json_data['page'] == 2
    assert json_data['total'] == 12

    response = testapp.get(f"/users?per_page=5&page=1", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 5
    assert json_data['page'] == 1
    assert json_data['total'] == 12

    response = testapp.get(f"/users?per_page=5&page=2", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 5
    assert json_data['page'] == 2
    assert json_data['total'] == 12

    response = testapp.get(f"/users?per_page=5&page=3", headers={'x-access-token': token})
    json_data = response.get_json()

    assert len(json_data['users']) == 2
    assert json_data['page'] == 3
    assert json_data['total'] == 12

def test_delete_user_as_admin(testapp, db_handle):
    user_to_delete = User(email='sevaaborrar@gmail.com',
                    display_name='Se Borra',
                    phone_number='11111111111',
                    image_location='http://www.youtube.com',
                    admin=False)

    user_admin = User(email='admin@gmail.com',
                    display_name='Admin',
                    phone_number='25642346456',
                    image_location='http://www.youtube.com',
                    admin=True)

    db_handle.session.add(user_to_delete)
    db_handle.session.add(user_admin)
    db_handle.session.commit()
    
    auth_service.setData({'email': user_admin.email,
                        'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'})
    
    response = testapp.delete(f"/users/{user_to_delete.id}", headers={'x-access-token': token})
    json_data = response.get_json()

    db.session.delete(user_admin)
    db_handle.session.commit()

    assert json_data['message'] == 'User deleted.'
    assert response.status_code == 200

def test_delete_own_user(testapp, db_handle):
    user = User(email='sevaaborrar@gmail.com',
                    display_name='Se Borra',
                    phone_number='11111111111',
                    image_location='http://www.youtube.com',
                    admin=False)

    db_handle.session.add(user)
    db_handle.session.commit()
    
    auth_service.setData({'email': user.email,
                        'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'})
    
    response = testapp.delete(f"/users/{user.id}", headers={'x-access-token': token})
    json_data = response.get_json()

    assert json_data['message'] == 'User deleted.'
    assert response.status_code == 200

def test_delete_another_user_with_no_admin_user(testapp, db_handle):
    user_to_delete = User(email='sevaaborrar@gmail.com',
                    display_name='Se Borra',
                    phone_number='11111111111',
                    image_location='http://www.youtube.com',
                    admin=False)

    user = User(email='user@gmail.com',
                    display_name='User',
                    phone_number='2454564652',
                    image_location='http://www.youtube.com',
                    admin=False)

    db_handle.session.add(user_to_delete)
    db_handle.session.add(user)
    db_handle.session.commit()
    
    auth_service.setData({'email': user.email,
                        'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'})
    
    response = testapp.delete(f"/users/{user_to_delete.id}", headers={'x-access-token': token})
    json_data = response.get_json()

    assert json_data['message'] == 'Only admins can delete other users.'
    assert response.status_code == 401
 
def test_delete_inexistent_user_as_admin(testapp, db_handle):
    user_admin = User(email='admin@gmail.com',
                    display_name='Admin',
                    phone_number='25642346456',
                    image_location='http://www.youtube.com',
                    admin=True)

    db_handle.session.add(user_admin)
    db_handle.session.commit()
    
    auth_service.setData({'email': user_admin.email,
                        'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'})
    
    inexistent_user_id = 25646
    response = testapp.delete(f"/users/{inexistent_user_id}", headers={'x-access-token': token})
    json_data = response.get_json()

    db.session.delete(user_admin)
    db_handle.session.commit()

    assert json_data['message'] == f'No user found with ID: {inexistent_user_id}.'
    assert response.status_code == 404