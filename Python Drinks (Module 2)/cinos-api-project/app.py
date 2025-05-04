# Command to get order: curl -X GET http://127.0.0.1:5000/order
# Command to add to order: curl -X POST http://127.0.0.1:5000/order \-H "Content-Type: application/json" \-d '{"size": "Medium", "base": "Sbrite", "flavors": ["lemon", "lime"]}'
# Command to delete a specific item in the order: curl -X DELETE http://127.0.0.1:5000/order/0

from flask import Flask, request, jsonify

# Initialize Flask
app = Flask(__name__)

# All the available bases, flavors, sizes, and their costs
bases = ["water", "sbrite", "pokeacola", "mr. salt", "hill fog", "leaf wine"]
flavors = ["lemon", "cherry", "strawberry", "mint", "blueberry", "lime"]
sizes = {
    "small": 1.50,
    "medium": 1.75,
    "large": 2.05,
    "mega": 2.15
}

# Additional costs
flavorCost = 0.15  # Cost for additional flavors
taxRate = 0.0725   # Tax rate


class Drink:
    """
    Each drink in the order.

    Attributes:
        _base (str): base of the drink.
        _flavors (list): list for flavors added to the drink.
        _size (str): size of the drink.
    """

    def __init__(self, size):
        """
        Initializes the drink object, requires a size.

        Args:
            size (str): size of the drink.
        """
        self._base = None
        self._flavors = []
        self._size = None
        self.set_size(size)

    def get_base(self):
        """
        Returns base of the drink.

        Returns:
            str: base of the drink, or none if not set.
        """
        return self._base.lower() if self._base else None

    def get_flavors(self):
        """
        Returns list of flavors added to the drink.

        Returns:
            list: the list of flavors.
        """
        return self._flavors

    def set_base(self, base):
        """
        Sets the base of the drink if its valid.

        Args:
            base (str): the base.

        Returns:
            str: invalid base if the base isn't in the list of available bases.
        """
        if base.lower() in bases:
            self._base = base
        else:
            return "Invalid base"

    def add_flavor(self, flavor):
        """
        Adds a flavor to the drink if its valid and not been added already.

        Args:
            flavor (str): flavor to add.

        Returns:
            str: invalid flavor if the flavor isn't in the flavors list.
        """
        if flavor.lower() in flavors and flavor.lower() not in self._flavors:
            self._flavors.append(flavor.lower())
        elif flavor.lower() not in flavors:
            return "Invalid flavor"

    def set_size(self, size):
        """
        Sets the size of the drink if its valid.

        Args:
            size (str): size to set.

        Returns:
            str: invalid size if the size isn't in the size list.
        """
        if size.lower() in sizes:
            self._size = size.lower()
        else:
            return "Invalid size"

    def get_size(self):
        """
        Returns the size of the drink.

        Returns:
            str: size of the drink.
        """
        return self._size

    def get_total(self):
        """
        Calculates the total cost of the drink based on size and added flavors.

        Returns:
            float: total drink cost.
        """
        if not self._size:
            return 0
        sizeCost = sizes[self._size]
        flavorCostTotal = len(self._flavors) * flavorCost
        return round(sizeCost + flavorCostTotal, 2)


class Order:
    """
    The total order of drinks.

    Attributes:
        _items (list): drinks in the order.
    """

    def __init__(self):
        """
        Initializes the order object with no drinks.
        """
        self._items = []

    def add_drink(self, drink):
        """
        Adds drink to the order.

        Args:
            drink (Drink): which drink to add.
        """
        self._items.append(drink)

    def remove_drink(self, index):
        """
        Removes a drink from the order using the listindex.

        Args:
            index (int): index of the drink to remove.

        Returns:
            str: "Invalid index" if the number isn't in the range of the drinks.
        """
        if index >= 0 and index < len(self._items):
            self._items.pop(index)
        else:
            return "Invalid index"

    def get_receipt(self):
        """
        AMkes a receipt for the order.

        Returns:
            list: all the information for each drink in the order.
        """
        receipt = []
        for i, drink in enumerate(self._items):
            receipt.append({
                "index": i,
                "base": drink.get_base(),
                "size": drink.get_size(),
                "flavors": drink.get_flavors(),
                "total": drink.get_total()
            })
        return receipt

    def get_total(self):
        """
        Calculates total cost of the order before tax.

        Returns:
            float: total cost of the order.
        """
        return round(sum(drink.get_total() for drink in self._items), 2)

    def get_total_after_tax(self):
        """
        Calculates total cost after tax.

        Returns:
            dict: dictionary containing the subtotal, tax, and total after tax.
        """
        total = self.get_total()
        tax = round(total * taxRate, 2)
        return {
            "subtotal": total,
            "tax": tax,
            "total_after_tax": round(total + tax, 2)
        }


# Create a order object
order = Order()


@app.route('/')
def home():
    """
    Home route with instructions for getting to the right webpage.

    Returns:
        dict: message with instructions.
    """
    return jsonify({"message": "add /order in the url to use"})


@app.route('/order', methods=['GET'])
def get_order():
    """
    Gets the current order, including receipt and totals.

    Returns:
        dict: receipt, totals, and the number of items in the order.
    """
    return jsonify({
        "items": order.get_receipt(),
        "totals": order.get_total_after_tax(),
        "num_items": len(order._items)
    })


@app.route('/order', methods=['POST'])
def add_drink():
    """
    Adds new drink to the order.

    Returns:
        dict: success message or error message depending on if the input is valid or not.
    """
    data = request.json
    size = data.get("size")
    if not size:
        return jsonify({"error": "Size is required"}), 400

    drink = Drink(size)
    baseError = drink.set_base(data.get("base"))
    if baseError:
        return jsonify({"error": baseError}), 400

    for flavor in data.get("flavors", []):
        flavorError = drink.add_flavor(flavor)
        if flavorError:
            return jsonify({"error": flavorError}), 400

    order.add_drink(drink)
    return jsonify({"message": "Drink added successfully."}), 201


@app.route('/order/<int:index>', methods=['DELETE'])
def remove_drink(index):
    """
    Removes a drink from the order using index in the url.

    Returns:
        dict: A success message or an error message.
    """
    error = order.remove_drink(index)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Drink removed successfully."}), 200


if __name__ == '__main__':
    app.run(debug=True)