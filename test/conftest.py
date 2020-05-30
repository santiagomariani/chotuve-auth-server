from app import create_app
import pytest
from testing.postgresql import Postgresql
#import psycopg2
import os
import tempfile

@pytest.yield_fixture(scope='session')
def flask_app():
    app = create_app('testing')
    #app.config["TESTING"] = True
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()

@pytest.fixture(scope='session')
def testapp(flask_app):
    print(type(flask_app.test_client()))
    return flask_app.test_client()

from controllers import controllers
from handlers import *
"""
@pytest.fixture(scope='function', autouse=True)
def db_handle(app):
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    
    db.init_app(app)
    db.create_all()
       
    yield db
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
"""
"""
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = User(email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')
    user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()


    

    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db
    
    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)



from app import create_app

@pytest.fixture(scope='session')
def app():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True

"""