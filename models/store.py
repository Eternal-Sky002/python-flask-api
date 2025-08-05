from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    provinsi = db.Column(db.String(255), unique = False, nullable = False)
    kabupaten_kota = db.Column(db.String(255), unique = False, nullable = False)
    kecamatan = db.Column(db.String(255), unique = False, nullable = False)
    kelurahan = db.Column(db.String(255), unique = False, nullable = False)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")