from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    provinsi = fields.Str(required = True)
    kabupaten_kota = fields.Str(required = True)
    kecamatan = fields.Str(required = True)
    kelurahan = fields.Str(required = True)

class PlainItemSchema(Schema):
    # only used when returning the data
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)
    qty = fields.Int(required = True)

class PlainTagSchema(Schema):  
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required = True, load_only = True)
    # nested to Plain Class to avoid recursive nesting
    store = fields.Nested(PlainStoreSchema(), dump_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class StoreSchema(PlainStoreSchema):
    # nested to Plain Class to avoid recursive nesting
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class TagSchema(PlainTagSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only = True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required = True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    qty = fields.Int()

class StoreUpdateSchema(Schema):
    name = fields.Str()