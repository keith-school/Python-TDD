# Testing the order class

from main import Order, Drink

# Testing retrieving the reciept while empy
def test_get_receipt_empty():
    order = Order()
    assert order.get_receipt() == []

# Testing the reciept while it has items
def test_get_receipt_with_items():
    order = Order()
    drink = Drink("Medium")
    drink.set_base("sbrite")
    drink.add_flavor("lemon")
    order.add_item(drink)
    receipt = order.get_receipt()
    assert len(receipt) == 1
    assert receipt[0]["base"] == "sbrite"
    assert receipt[0]["size"] == "medium"
    assert receipt[0]["flavors"] == ["lemon"]
    assert receipt[0]["total"] == drink.get_total()

# Testing order total without added drinks
def test_get_total_empty():
    order = Order()
    assert order.get_total() == 0

# Testing total with drinks ordered
def test_get_total_with_items():
    order = Order()
    drink1 = Drink("Small")
    drink1.set_base("Sbrite")
    drink2 = Drink("Large")
    drink2.set_base("Pokeacola")
    order.add_item(drink1)
    order.add_item(drink2)
    assert order.get_total() == round(drink1.get_total() + drink2.get_total(), 2)

# Testing order tax with no drinks
def test_get_total_after_tax_empty():
    order = Order()
    totals = order.get_total_after_tax()
    assert totals["subtotal"] == 0
    assert totals["tax"] == 0
    assert totals["total_after_tax"] == 0

# Testing order tax with drinks
def test_get_total_after_tax_with_items():
    order = Order()
    drink = Drink("Mega")
    drink.set_base("Hill Fog")
    drink.add_flavor("mint")
    order.add_item(drink)
    totals = order.get_total_after_tax()
    assert totals["subtotal"] == drink.get_total()
    assert totals["tax"] == round(drink.get_total() * 0.0725, 2)
    assert totals["total_after_tax"] == round(drink.get_total() + totals["tax"], 2)

# Testing removing the drinks with a drink
def test_remove_drink_valid():
    order = Order()
    drink = Drink("Small")
    order.add_item(drink)
    order.remove_item(0)
    assert len(order.get_receipt()) == 0

# Testing removing drinks without any drinks
def test_remove_drink_invalid():
    order = Order()
    result = order.remove_item(0)
    assert result == "Invalid index"