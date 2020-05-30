import pytest
from test.conftest import *
from models.models import User

"""
def sum(x, y):
    return x + y

def test_answer():
    assert sum(3, 4) == 7

def test_home_page(testapp):
    response = testapp.post('/ping')
    assert response.status_code == 200
    user = User.query.filter_by(email="sebastianperez@gmail.com").first()
    assert user
    print(user.display_name)
"""

def test_simple_ping(testapp):
    response = testapp.post('/reset-codes')
    print(response.data)
    assert response.status_code == 200