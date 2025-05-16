# Testing the food class

from main import Food, foods, toppings
import math

# Testing getting food type with no type set
def test_get_type_empty():
    food = Food("hotdog")
    assert food.get_type() == "hotdog"

# Testing setting valid food types
def test_set_type_valid():
    food = Food("hotdog")
    food.set_type("corndog")
    assert food.get_type() == "corndog"

# Testing setting invalid food types
def test_set_type_invalid():
    food = Food("hotdog")
    result = food.set_type("InvalidFood")
    assert result == "Invalid food type"
    assert food.get_type() == "hotdog"

# Testing getting toppings with no added toppings
def test_get_toppings_empty():
    food = Food("hotdog")
    assert food.get_toppings() == []

# Testing if toppings work
def test_add_topping_valid():
    food = Food("hotdog")
    food.add_topping("ketchup")
    assert food.get_toppings() == ["ketchup"]

# Testing multiple toppings being added
def test_add_multiple_toppings():
    food = Food("hotdog")
    food.add_topping("ketchup")
    food.add_topping("mustard")
    assert food.get_toppings() == ["ketchup", "mustard"]

# Testing duplicate toppings
def test_add_duplicate_topping():
    food = Food("hotdog")
    food.add_topping("ketchup")
    food.add_topping("ketchup")
    assert food.get_toppings() == ["ketchup"]

# Testing invalid toppings
def test_add_topping_invalid():
    food = Food("hotdog")
    result = food.add_topping("InvalidTopping")
    assert result == "Invalid topping"
    assert food.get_toppings() == []

# Testing total cost without toppings
def test_get_total_no_toppings():
    food = Food("hotdog")
    assert food.get_total() == foods["hotdog"]

# Testing if free toppings affect cost
def test_get_total_with_toppings():
    food = Food("hotdog")
    food.add_topping("ketchup")
    food.add_topping("mustard")
    assert food.get_total() == foods["hotdog"]

# Testing if paid topping work
def test_get_total_with_paid_toppings():
    food = Food("hotdog")
    food.add_topping("chili")
    food.add_topping("bacon bits")
    expected_total = foods["hotdog"] + toppings["chili"] + toppings["bacon bits"]
    assert round(food.get_total(), 2) == round(expected_total, 2)