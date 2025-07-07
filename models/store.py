from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    # lazy = "dynamic" adalah untuk menghindari pemanggilan data secara langsung, hanya ketika dilakukan request
    items = db.relationship("ItemModel", back_populates = "store", lazy = "dynamic", cascade = "all, delete")