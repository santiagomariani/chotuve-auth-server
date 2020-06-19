import os

from app import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


from controllers import controllers

if __name__ == '__main__':
    app.run()