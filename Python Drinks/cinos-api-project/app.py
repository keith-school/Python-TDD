
from flask import Flask, request, jsonify

app = Flask(__name__)
bases = ["Water", "Sbrite", "Pokeacola", "Mr. Salt", "Hill Fog", "Leaf Wine"]
flavors = ["lemon", "cherry", "strawberry", "mint", "blueberry", "lime"]

class Drink:
    def __init__(self):
        self._base = None
        self._flavors = [] 

    def get_base(self):
        return self._base

    def get_flavors(self):
        return self._flavors

    def set_base(self, base):
        if base in bases:
            self._base = base
        else:
            return "Invalid base"

    def add_flavor(self, flavor):
        if flavor in flavors and flavor not in self._flavors:
            self._flavors.append(flavor)
        elif flavor not in flavors:
            return "Invalid flavor"

class Order:
    def __init__(self):
        self._items = []

    def add_drink(self, drink):
        self._items.append(drink)

    def remove_drink(self, index):
        if index >= 0 and index < len(self._items):
            self._items.pop(index)
        else:
            return "Invalid index"

    def get_receipt(self):
        receipt = []
        for i, drink in enumerate(self._items):
            receipt.append({
                "index": i,
                "base": drink.get_base(),
                "flavors": drink.get_flavors()
            })
        return receipt

    def get_total(self):
        return len(self._items) * 5

    def get_num_items(self):
        return len(self._items)

order = Order()

@app.route('/')
def home():
    return jsonify({"message": "add /order in the url to use"})

@app.route('/order', methods=['GET'])
def get_order():
    return jsonify({
        "items": order.get_receipt(),
        "total": order.get_total(),
        "num_items": order.get_num_items()
    })

@app.route('/order', methods=['POST'])
def add_drink():
    data = request.json
    drink = Drink()
    base_error = drink.set_base(data.get("base"))
    if base_error:
        return jsonify({"error": base_error}), 400

    for flavor in data.get("flavors", []):
        flavor_error = drink.add_flavor(flavor)
        if flavor_error:
            return jsonify({"error": flavor_error}), 400

    order.add_drink(drink)
    return jsonify({"message": "Drink added successfully."}), 201

@app.route('/order/<int:index>', methods=['DELETE'])
def remove_drink(index):
    error = order.remove_drink(index)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Drink removed successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)