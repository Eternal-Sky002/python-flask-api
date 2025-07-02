import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)

@app.get("/stores") # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/stores")
def create_store():
    store_data = request.get_json()

    # form validation
    if(
        "name" not in store_data
    ):
        abort(400, message = "Bad Request. 'name' is required")
    
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

@app.get("/items") # http://127.0.0.1:5000/store
def get_items():
    return {"items": list(items.values())}

@app.post("/items")
def create_item():
    item_data = request.get_json()

    # form validation
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400, message = "Bad Request. 'price', 'store_id', and 'name' is required")

    # check if the item already exists
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message = f"Item already exists.")

    # check if the store exists in database
    if item_data["store_id"] not in stores:
        abort(404, message = "Store not found")
    
    # using uuid for the id
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message = "Store not found")

@app.put("/stores/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()

    # form validation
    if(
        "name" not in store_data
    ):
        abort(400, message = "Bad Request. 'name' is required")
    
    # check if another store already has the new name (excluding current store)
    for existing_store_id, store in stores.items():
        if(
            existing_store_id != store_id
            and store_data["name"] == store["name"]
        ):
            abort(400, message = f"Store with name '{store_data['name']}' already exists.")
    
    try:
        store = stores[store_id]
        # to replace the values of a dictionary, use |=
        store |= store_data

        return store
    except KeyError:
        abort(404, message = "Store not found")

@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
    try:
        # Check if store exists first
        if store_id not in stores:
            abort(404, message = "Store not found")
        
        # Find and delete all items belonging to this store to maintain data integrity
        items_to_delete = [item_id for item_id, item in items.items() if item["store_id"] == store_id]
        for item_id in items_to_delete:
            del items[item_id]
        
        # Now delete the store
        del stores[store_id]
        
        if items_to_delete:
            return {"message": f"Store deleted along with {len(items_to_delete)} associated items"}
        else:
            return {"message": "Store deleted"}
    except KeyError:
        abort(404, message = "Store not found")

@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message = "Item not found")

@app.put("/items/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    # form validation
    if(
        "price" not in item_data
        or "name" not in item_data
    ):
        abort(400, message = "Bad Request. 'price', and 'name' is required")
    
    # validate store_id if it's being updated
    if "store_id" in item_data and item_data["store_id"] not in stores:
        abort(404, message = "Store not found")
    
    try:
        item = items[item_id]
        # to replace the values of a dictionary, use |=
        item |= item_data

        return item
    except KeyError:
        abort(404, message = "Item not found")

@app.delete("/items/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message = "Item not found")
