from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel
from ecc.compute import scalar_mult

# every resource should be a class 
# no need jsonify with flask restful, just return dictionary

class Key(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('current_user', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('friend_user', type=str, required=True, help="you need a valid friend name")
    #@jwt_required() 
    #---------- TO BE REVIEWED----------#
    @jwt_required() 
    def post(self):
        data = Key.parser.parse_args()
        currentUser = UserModel.find_by_username(data['current_user'])
        friendUser = UserModel.find_by_username(data['friend_user'])
        if currentUser and friendUser:
            # print("friend user")
            mySecretKey = int(currentUser.secret_key)
            friendPublicKey= (int(friendUser.public_key_x), int(friendUser.public_key_y ))
            # print(friendPublicKey)
            sharedSecret = scalar_mult(mySecretKey , friendPublicKey)
            return {'key': str(sharedSecret[0])}
        elif currentUser:
            return {'message': 'friend user not found'}, 400
        else:
            return {'message': 'currentUser not found'}, 400