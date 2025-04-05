from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data (in-memory dictionary)
items = {
	1: {"name": "Laptop", "price": 1200},
	2: {"name": "Mouse", "price": 25},
	3: {"name": "Keyboard", "price": 75}
}

# --- Basic Routes ---

@app.route('/')
def home():
	return "<h1>Welcome to the Flask Web Server!</h1>"

@app.route('/hello/<name>')
def hello(name):
	return f"Hello, {name}!"

# --- API Endpoints for Items ---

# GET all items
@app.route('/api/items', methods=['GET'])
def get_all_items():
	return jsonify(items)

# GET a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
	if item_id in items:
		return jsonify(items[item_id])
	return jsonify({"error": "Item not found"}), 404

# POST a new item
@app.route('/api/items', methods=['POST'])
def create_item():
	data = request.get_json()
	if not data or 'name' not in data or 'price' not in data:
		return jsonify({"error": "Missing name or price"}), 400

	new_id = max(items.keys()) + 1 if items else 1
	items[new_id] = {"name": data['name'], "price": data['price']}
	return jsonify(items[new_id]), 201  # 201 Created

# PUT (update) an existing item by ID
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
	if item_id not in items:
		return jsonify({"error": "Item not found"}), 404

	data = request.get_json()
	if not data or 'name' not in data or 'price' not in data:
		return jsonify({"error": "Missing name or price in update data"}), 400

	items[item_id]['name'] = data['name']
	items[item_id]['price'] = data['price']
	return jsonify(items[item_id])

# DELETE an item by ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
	if item_id not in items:
		return jsonify({"error": "Item not found"}), 404

	del items[item_id]
	return jsonify({"message": f"Item {item_id} deleted"}), 200

if __name__ == '__main__':
	app.run(debug=True)