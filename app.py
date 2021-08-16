import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from security import authenticate, identity
from resources.user import UserRegister
from resources.sharedkey import Key
from db import db

app=Flask(__name__)
#_--------------------------------------gonna be at root folder-------
# database_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
#changed_url = database_url.replace("postgres://", "postgresql://")
# app.config['SQLALCHEMY_DATABASE_URI'] = changed_url

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key = 'myat'
database_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
changed_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = changed_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'myat'
api = Api(app)
cors = CORS(app, resources={r"/.*": {"origins": "*"}})

# @app.before_first_request
# def create_tables():
#     # creates the table if they don't exist
#     db.create_all()



jwt = JWT(app, authenticate, identity)  # jwt creates new endpoint /auth

api.add_resource(Key, '/getKey')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)