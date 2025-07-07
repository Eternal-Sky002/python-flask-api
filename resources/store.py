import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import StoreSchema, StoreUpdateSchema
from models import StoreModel

blp = Blueprint("stores", __name__, description = "Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_id, store_data):
        store = StoreModel.query.get_or_404(store_id)
        store.name = store_data["name"]

        db.session.add(store)
        db.session.commit()

        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many = True))
    def get(self):
        stores = StoreModel.query.all()
        return stores
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting the store.")
        return store, 201