# Testing the IceStorm class

from main import IceStorm, iceStorms, mixIns

# Testing setting valid flavor
def test_set_flavor_valid():
    ice_storm = IceStorm("mint chocolate chip")
    assert ice_storm.get_flavor() == "mint chocolate chip"

# Testing setting invalid flavor
def test_set_flavor_invalid():
    ice_storm = IceStorm("invalid flavor")
    assert ice_storm.get_flavor() is None

# Testing adding a valid mix in
def test_add_mix_in_valid():
    ice_storm = IceStorm("chocolate")
    ice_storm.add_mix_in("cherry")
    assert ice_storm.get_mix_ins() == ["cherry"]

# Testing adding multiple mix ins
def test_add_multiple_mix_ins():
    ice_storm = IceStorm("vanilla bean")
    ice_storm.add_mix_in("cherry")
    ice_storm.add_mix_in("storios")
    assert ice_storm.get_mix_ins() == ["cherry", "storios"]

# Testing duplicate mix ins
def test_add_duplicate_mix_in():
    ice_storm = IceStorm("banana")
    ice_storm.add_mix_in("cherry")
    ice_storm.add_mix_in("cherry")
    assert ice_storm.get_mix_ins() == ["cherry"]

# Testing invalid mix in
def test_add_mix_in_invalid():
    ice_storm = IceStorm("butter pecan")
    result = ice_storm.add_mix_in("invalid mix in")
    assert result == "Invalid mix in"
    assert ice_storm.get_mix_ins() == []

# Testing cost with no mix ins
def test_get_total_no_mix_ins():
    ice_storm = IceStorm("s'more")
    assert ice_storm.get_total() == iceStorms["s'more"]

# Testing cost with free mix ins
def test_get_total_with_free_mix_ins():
    ice_storm = IceStorm("mint chocolate chip")
    ice_storm.add_mix_in("cherry")
    ice_storm.add_mix_in("whipped cream")
    assert ice_storm.get_total() == iceStorms["mint chocolate chip"]

# Testing cost with paid mix ins
def test_get_total_with_paid_mix_ins():
    ice_storm = IceStorm("chocolate")
    ice_storm.add_mix_in("storios")
    ice_storm.add_mix_in("t&t's")
    expected_total= iceStorms["chocolate"] + mixIns["storios"] + mixIns["t&t's"]
    assert round(ice_storm.get_total(), 2) == round(expected_total, 2)