from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    # only used when returning the data
    id = fields.Str(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required = True)

class StoreUpdateSchema(Schema):
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Str(required = True, load_only = True)
    # nested to Plain Class to avoid recursive nesting
    store = fields.Nested(PlainStoreSchema(), dump_only = True)

class StoreSchema(PlainStoreSchema):
    # nested to Plain Class to avoid recursive nesting
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)