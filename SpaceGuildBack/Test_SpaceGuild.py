
import location as loc
import spaceshipComponent as spc
import spaceship as sp
from item import Item
from player import Player

# test function must begin with test_ !!!
# this file name must start with Test_ !!!
# debug by 

def test_add_item():
	cargo = spc.Cargo('basic cargo', 0)
	
	testitem = Item('basic item','nowhere',1,50)

	result = spc.add_item(cargo, testitem)
	
	assert result
	assert len(cargo['items']) == 1
	assert spc.can_fit_item(cargo, cargo['capacity'] - spc.total_cargo_weight(cargo))
	pass

def test_take_damage():
	cargo = spc.Cargo('basic cargo', 0)
	spc.apply_damage(cargo, 5)
	assert cargo['health'] == 95
	pass

def test_locations_are_created_correctly():
	loc.locationhandler.clear()
	loc.addnewlocation('earth')
	assert len(loc.locationhandler.keys()) == 1
	loc.locationhandler.clear()
	pass


def test_locations_link_correctly():
	loc.locationhandler.clear()
	loc.addnewlocation('earth')
	loc.addnewlocation('mars')
	loc.addnewlocation('jupiter')
		
	loc.linklocations('earth','mars')
	loc.linklocations('mars','jupiter')
	
	assert loc.locationhandler['earth']['links'].__contains__('mars')
	assert loc.locationhandler['mars']['links'].__contains__('earth')
	assert not loc.locationhandler['earth']['links'].__contains__('jupiter')

	loc.locationhandler.clear()
	pass

def test_make_player():
	p1 = Player()
	assert p1 != None