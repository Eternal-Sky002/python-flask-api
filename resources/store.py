import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description = "Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message = "Store not found")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_id, store_data):
        try:
            store = stores[store_id]
            # to replace the values of a dictionary, use |=
            store |= store_data

            return store
        except KeyError:
            abort(404, message = "Store not found")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message = "Store not found")

@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many = True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # check if the store already exists
        for store in stores.values():
            if(
                store_data["name"] == store["name"]
            ):
                abort(400, message = f"Store already exists.")

        # using uuid for the id
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201