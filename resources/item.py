from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field can't be left blank!")
    parser.add_argument('store_id', type=int, required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            return {'item': item.json()}, 202

        return {'message': f'Item {name} not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': f'An item with the name - {name} already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_item_to_db()
        except:
            return {"message": "something went wrong!"}, 500

        return item.json(), 201

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        try:
            if item:
                item.price = data['price']
            else:
                item = ItemModel(name, **data)

            item.save_item_to_db()
            return item.json(), 200

        except:
            return {"message": "something went wrong while updating!"}, 500

    def delete(self, name):

        item = ItemModel.find_by_name(name)

        try:
            if item:
                item.delete_item_from_db()
                return {'message': 'Deleted successfully'}, 200
            else:
                return {'message': f'Item {name} not found'}, 404
        except:
            return {'message': f'error occured while deleting {name}'}, 500


class ItemList(Resource):
    def get(self):
        # return {"items": [item.json() for item in ItemModel.get_all_items()]}
        return {"items": list(map(lambda item: item.json(), ItemModel.get_all_items()))}
