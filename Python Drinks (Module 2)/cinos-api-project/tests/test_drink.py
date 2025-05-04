# Testing the drink class

from app import Drink, bases, flavors, sizes

# Testing getting empty base
def test_get_base():
    drink = Drink("Small")
    assert drink.get_base() is None

# Testing setting a valid base
def test_set_base_valid():
    drink = Drink("Small")
    drink.set_base("Sbrite")
    assert drink.get_base() == "sbrite"

# Testing setting a base that isnt valid
def test_set_base_invalid():
    drink = Drink("Small")
    result = drink.set_base("InvalidBase")
    assert result == "Invalid base"
    assert drink.get_base() is None

# Testing getting empty flavors
def test_get_flavors():
    drink = Drink("Small")
    assert drink.get_flavors() == []
    
# Testing adding valid extra flavor
def test_add_flavor_valid():
    drink = Drink("Small")
    drink.add_flavor("lemon")
    assert drink.get_flavors() == ["lemon"]

# Testing adding multiple of the same extra flavor
def test_add_flavor_duplicate():
    drink = Drink("Small")
    drink.add_flavor("lemon")
    drink.add_flavor("lemon")
    assert drink.get_flavors() == ["lemon"]

# Testing adding invalid extra flavor
def test_add_flavor_invalid():
    drink = Drink("Small")
    result = drink.add_flavor("InvalidFlavor")
    assert result == "Invalid flavor"
    assert drink.get_flavors() == []

# Testing getting a size
def test_get_size():
    drink = Drink("Large")
    assert drink.get_size() == "large"

# TEsting setting a valid size
def test_set_size_valid():
    drink = Drink("Small")
    drink.set_size("Medium")
    assert drink.get_size() == "medium"

# Testing an invalid size
def test_set_size_invalid():
    drink = Drink("Small")
    result = drink.set_size("InvalidSize")
    assert result == "Invalid size"
    assert drink.get_size() == "small"

# Testing total with no tax or extra flavors
def test_get_total_no_flavors():
    drink = Drink("Medium")
    drink.set_base("Sbrite")
    assert drink.get_total() == sizes["medium"]

# Testing toal with with no tax but extra flavors
def test_get_total_with_flavors():
    drink = Drink("Medium")
    drink.set_base("Sbrite")
    drink.add_flavor("lemon")
    drink.add_flavor("lime")
    assert drink.get_total() == round(sizes["medium"] + 2 * 0.15, 2)