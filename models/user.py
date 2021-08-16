from db import db
from ecc.compute import make_keypair



class UserModel(db.Model):
    __tablename__ = 'users'
    #----- id is auto incrementing
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    secret_key = db.Column(db.String(80))
    public_key_x = db.Column(db.String(100))
    public_key_y = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        secretKey, publicKey = make_keypair()
        self.secret_key = str(secretKey)
        self.public_key_x = str(publicKey[0])
        self.public_key_y = str(publicKey[1])


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()