from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    price = db.Column(db.Float(precision = 2), unique = False, nullable = False)
    # relasi dengan table stores dan foreign key dengan kolom id
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique = False, nullable = False)
    # memanggil StoreModel karena ada relasi dengan table stores
    # back_populates = "items" adalah nama relasi dari table items
    store = db.relationship("StoreModel", back_populates = "items")
    tags = db.relationship("TagModel", back_populates = "items", secondary = "items_tags")