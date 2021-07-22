from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from auth import authenticate, identity

app = Flask(__name__, static_url_path='', static_folder='build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'My secret key'
CORS(app, resources={
     r"/*": {"origins": ["https://flaskstore.azurewebsites.net"]}})
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

jwt = JWT(app, authenticate, identity)  # create a route /auth


@app.route('/', defaults={'path': ''})
def serve_react(path):
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
