import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db

blp = Blueprint("items", __name__, description = "Operations on items")

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    # the position matters
    @blp.response(200, ItemSchema)
    def put(self, item_id, item_data):      
        item = ItemModel.query.get_or_404(item_id)
        item.price = item_data["price"]
        item.name = item_data["name"]

        db.session.add(item)
        db.session.commit()

        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
        
@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many = True))
    def get(self):
        items = ItemModel.query.all()
        return items
    
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