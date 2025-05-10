# Command to get order: curl -X GET http://127.0.0.1:5000/order
# Command to add drink to order: curl -X POST http://127.0.0.1:5000/order \-H "Content-Type: application/json" \-d '{"size": "large", "base": "Sbrite", "flavors": ["lemon", "lime"]}'
# Command to add food to order: curl -X POST http://127.0.0.1:5000/order/food \-H "Content-Type: application/json" \-d '{"foodType": "ice cream", "toppings": ["whipped cream", "cherry"]}'
# Command to add food to order: curl -X POST http://127.0.0.1:5000/order/food \-H "Content-Type: application/json" \-d '{"foodType": "nacho chips", "toppings": ["nacho cheese", "chili"]}'
# Command to delete a specific item in the order: curl -X DELETE http://127.0.0.1:5000/order/0

from flask import Flask, request, jsonify

# Initialize Flask
app = Flask(__name__)

# All the available bases, flavors, sizes, and their costs
foods = {
    "hotdog": 2.30, 
    "corndog": 2.00, 
    "ice cream": 3.00, 
    "onion rings": 1.75, 
    "french fries": 1.50, 
    "tater tots": 1.70, 
    "nacho chips": 1.90
}
toppings = {
    "cherry": 0.00, 
    "whipped cream": 0.00, 
    "caramel sauce": 0.50, 
    "chocolate sauce": 0.50, 
    "nacho cheese": 0.30, 
    "chili": 0.60, 
    "bacon bits": 0.30, 
    "ketchup": 0.00, 
    "mustard": 0.00
}
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

# Module 1-2 stuff
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
        Sets the base of the drink if it's valid.

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
        Adds a flavor to the drink if it's valid and not been added already.

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
        Sets the size of the drink if it's valid.

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

# Module 3 stuff
class Food:
    """
    Represents food item in the order.

    Attributes:
        _type (str): type of food.
        _toppings (list): toppings added to the food.
    """

    def __init__(self, foodType):
        """
        Initializes food object.

        Args:
            foodType (str): type of food.
        """
        self._type = None
        self._toppings = []
        self.set_type(foodType)

    def set_type(self, foodType):
        """
        Sets the type of food if valid.

        Args:
            foodType (str): sets type of food.

        Returns:
            str: invalid foor type if food type isn't in foods array.
        """
        if foodType.lower() in foods:
            self._type = foodType.lower()
        else:
            return "Invalid food type"

    def get_type(self):
        """
        Returns the type of food.

        Returns:
            str: type of food.
        """
        return self._type

    def add_topping(self, topping):
        """
        Adds a topping to the food if valid.

        Args:
            topping (str): topping to add.

        Returns:
            str: invalid topping if not in toppings list.
        """
        if topping.lower() in toppings and topping.lower() not in self._toppings:
            self._toppings.append(topping.lower())
        elif topping.lower() not in toppings:
            return "Invalid topping"

    def get_toppings(self):
        """
        Returns the list of toppings.

        Returns:
            list: list of toppings.
        """
        return self._toppings

    def get_total(self):
        """
        Calculates the total cost of a food item.

        Returns:
            float: cost of the food item.
        """
        if not self._type:
            return 0
        baseCost = foods[self._type]
        toppingCost = sum(toppings[topping] for topping in self._toppings)
        return round(baseCost + toppingCost, 2)

# Module 1-3 stuff
class Order:
    """
    The total order of drinks and food.

    Attributes:
        _items (list): both drinks and food in the order.
    """

    def __init__(self):
        """
        Initializes order object with no items.
        """
        self._items = []

    def add_item(self, item):
        """
        Adds an item to the order.

        Args:
            item: item to add.
        """
        self._items.append(item)

    def remove_item(self, index):
        """
        Removes an item from the order using the list index.

        Args:
            index (int): item to remove based on index.

        Returns:
            str: "Invalid index" if the number isn't in the correct range.
        """
        if index >= 0 and index < len(self._items):
            self._items.pop(index)
        else:
            return "Invalid index"

    def get_receipt(self):
        """
        Makes a receipt for the order.

        Returns:
            list: information for each item in the order.
        """
        receipt = []
        for i, item in enumerate(self._items):
            if isinstance(item, Drink):
                receipt.append({
                    "index": i,
                    "type": "drink",
                    "base": item.get_base(),
                    "size": item.get_size(),
                    "flavors": item.get_flavors(),
                    "total": item.get_total()
                })
            # Module 3 stuff
            elif isinstance(item, Food):
                receipt.append({
                    "type": "food",
                    "foodType": item.get_type(),
                    "toppings": item.get_toppings(),
                    "index": i,
                    "total": item.get_total()
                })
        return receipt

    def get_total(self):
        """
        Calculates total cost of the order before tax.

        Returns:
            float: total cost of the order.
        """
        return round(sum(item.get_total() for item in self._items), 2)

    def get_total_after_tax(self):
        """
        Calculates total cost after tax.

        Returns:
            dict: contains the subtotal, tax, and total after tax.
        """
        total = self.get_total()
        tax = round(total * taxRate, 2)
        return {
            "subtotal": total,
            "tax": tax,
            "total_after_tax": round(total + tax, 2)
        }


# Create an order object
order = Order()

# Module 1-3 stuff
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
    Adds a new drink to the order.

    Returns:
        dict: success or error message depending on if input is valid.
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

    order.add_item(drink)
    return jsonify({"message": "Drink added successfully."}), 201


@app.route('/order/food', methods=['POST'])
def add_food():
    """
    Adds a new food to the order.

    Returns:
        dict: success or error message depending on if the input is valid.
    """
    data = request.json
    foodType = data.get("foodType")
    if not foodType:
        return jsonify({"error": "Food type is required"}), 400

    food = Food(foodType)
    typeError = food.set_type(foodType)
    if typeError:
        return jsonify({"error": typeError}), 400

    for topping in data.get("toppings", []):
        toppingError = food.add_topping(topping)
        if toppingError:
            return jsonify({"error": toppingError}), 400

    order.add_item(food)
    return jsonify({"message": "Food added successfully."}), 201


@app.route('/order/<int:index>', methods=['DELETE'])
def remove_item(index):
    """
    Removes an item from the order with index in the URL.

    Returns:
        dict: success or an error message.
    """
    error = order.remove_item(index)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Item removed successfully."}), 200


if __name__ == '__main__':
    app.run(debug=True)