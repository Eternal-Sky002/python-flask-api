from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/stores/<string:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    @blp.doc(security=[{"bearerAuth": []}])
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag


@blp.route("/items/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tags/<string:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )