from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from auth import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'My secret key'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

jwt = JWT(app, authenticate, identity)  # create a route /auth


api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
