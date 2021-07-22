import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True, help="username field can't be left blank!")
    parser.add_argument('password', type=str,
                        required=True, help="password field can't be left blank!")

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "username already taken"}, 400

        try:
            user = UserModel(**data)
            user.save_user_to_db()

            return {"message": "user created successfully"}, 201
        except:
            return {"message": "error while creating user"}, 500
