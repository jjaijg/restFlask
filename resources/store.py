from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {"message": f'store {name} not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f'store {name} already exists'}, 400

        store = StoreModel(name)

        try:
            store.save_store_to_db()
            return store.json(), 201
        except:
            return {"message": f'error while creating store {name}'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": f'store {name} not found'}, 404

        try:
            store.delete_store_from_db()
            return {"message": f'store {name} deleted successfully'}
        except:
            return {"message": f'error while deleting store {name}'}, 500


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda store: store.json(), StoreModel.get_all_stores()))}
