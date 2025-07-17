from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt
from functools import wraps
from flask import abort

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db

blp = Blueprint("items", __name__, description = "Operations on items")

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                abort(403, message="You do not have access to this resource.")
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def put(self, item_id, item_data):      
        item = ItemModel.query.get_or_404(item_id)
        item.price = item_data["price"]
        item.name = item_data["name"]

        db.session.add(item)
        db.session.commit()

        return item
    
    @jwt_required()
    @role_required("ROLE_ADMIN")
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted"}
        
@blp.route("/items")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many = True))
    def get(self):
        items = ItemModel.query.all()
        return items
    
    @jwt_required()
    @role_required("ROLE_ADMIN")
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting the item.")

        return item, 201