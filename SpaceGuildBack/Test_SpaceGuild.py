from data import DataHandler
from location import Location
from ship import Ship
from item import Weapon, Cargo, Engine, Shield, Sensor, StealthCloak
from player import Player
from faction import Faction
import components
import actions
import program

# test function must begin with test_ !!!
# this file name must start with Test_ !!!

def setup_test_handler(dh):
	"""Helper to set up data handler for components and actions modules"""
	program.data_handler = dh
	components.data_handler = dh
	actions.data_handler = dh
	actions.clear_queues()  # Clear any leftover actions from previous tests

def test_locations_are_created_correctly():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	assert len(dh.Locations.keys()) == 1
	assert dh.Locations['earth']['name'] == 'earth'

def test_locations_link_correctly():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.add_location('jupiter')
	
	dh.double_link_locations('earth', 'mars')
	dh.double_link_locations('mars', 'jupiter')
	
	assert 'mars' in dh.Locations['earth']['links']
	assert 'earth' in dh.Locations['mars']['links']
	assert 'jupiter' not in dh.Locations['earth']['links']

def test_ship_creation_and_location():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	assert dh.Ships[1]['location'] == 'earth'
	assert 1 in dh.Locations['earth']['ship_ids']

def test_ship_movement():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	dh.move_ship_between_locations(1, 'earth', 'mars')
	
	assert dh.Ships[1]['location'] == 'mars'
	assert 1 not in dh.Locations['earth']['ship_ids']
	assert 1 in dh.Locations['mars']['ship_ids']

def test_add_item_to_cargo():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	cargo_comp = Cargo(100, 'basic cargo', 0, 10.0)
	dh.add_item(100, cargo_comp)
	dh.update_ship_component(1, 'cargo_id', 100)
	
	test_item = Weapon(200, 'laser', 0, 5.0)
	dh.add_item(200, test_item)
	dh.add_item_to_ship_cargo(1, 200)
	
	assert 200 in dh.Ships[1]['items']
	assert len(dh.Ships[1]['items']) == 1

def test_item_damage():
	dh = DataHandler(data_dir="test_data")
	
	weapon = Weapon(1, 'laser', 0, 5.0)
	dh.add_item(1, weapon)
	
	initial_health = dh.Items[1]['health']
	result = dh.damage_item(1, 10)
	
	assert result['health_damage'] == 10
	assert dh.Items[1]['health'] == initial_health - 10

def test_ship_hp_damage():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	initial_hp = dh.Ships[1]['hp']
	result = dh.damage_ship_hp(1, 20)
	
	assert result['hp_damage'] == 20
	assert dh.Ships[1]['hp'] == initial_hp - 20

def test_cargo_capacity_calculation():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	cargo_comp = Cargo(100, 'basic cargo', 0, 1.0)
	dh.add_item(100, cargo_comp)
	dh.update_ship_component(1, 'cargo_id', 100)
	
	capacity = components.get_ship_cargo_capacity(1)
	assert capacity == 100.0  # 100 * (1 + 0) * 1.0

def test_weapon_damage_calculation():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	weapon = Weapon(100, 'laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	damage = components.get_ship_weapon_damage(1)
	assert damage == 5.0

def test_action_queue():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Queue a move action
	result = actions.queue_action(1, 'move', 'mars')
	assert result == True
	assert 1 in actions.ship_to_node

def test_move_action_execution():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Queue and process move
	actions.queue_action(1, 'move', 'mars')
	stats = actions.process_tick()
	
	assert stats['moves'] == 1
	assert dh.Ships[1]['location'] == 'mars'

def test_attack_ship_action():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 10.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	# Create target
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	
	initial_hp = dh.Ships[2]['hp']
	
	# Queue and process attack
	actions.queue_action(1, 'attack_ship', 2)
	stats = actions.process_tick()
	
	assert stats['attack_ship'] == 1
	assert dh.Ships[2]['hp'] == initial_hp - 10.0

def test_make_player():
	p1 = Player('test_player', 1)
	assert p1 is not None
	assert 'ship_id' in p1
	assert p1['name'] == 'test_player'

def test_single_link_locations():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	
	dh.single_link_locations('earth', 'mars')
	
	assert 'mars' in dh.Locations['earth']['links']
	assert 'earth' not in dh.Locations['mars']['links']

def test_shield_pool_damage():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	dh.set_ship_shield_pool(1, 50.0)
	
	result = dh.damage_shield_pool(1, 30.0)
	
	assert result['shield_damage'] == 30.0
	assert result['remaining_shield'] == 20.0
	assert result['overflow_damage'] == 0.0
	assert dh.Ships[1]['shield_pool'] == 20.0

def test_shield_pool_overflow():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	dh.set_ship_shield_pool(1, 20.0)
	
	result = dh.damage_shield_pool(1, 30.0)
	
	assert result['shield_damage'] == 20.0
	assert result['remaining_shield'] == 0.0
	assert result['overflow_damage'] == 10.0

def test_attack_with_shields():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 25.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	# Create target with shields
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	dh.set_ship_shield_pool(2, 15.0)
	
	initial_hp = dh.Ships[2]['hp']
	
	# Attack should hit shields first, overflow to HP
	actions.queue_action(1, 'attack_ship', 2)
	stats = actions.process_tick()
	
	assert stats['attack_ship'] == 1
	assert dh.Ships[2]['shield_pool'] == 0.0
	assert dh.Ships[2]['hp'] == initial_hp - 10.0  # 25 damage - 15 shield = 10 hp damage

def test_attack_ship_component():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 15.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	# Create target with engine
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	engine = Engine(200, 'basic engine', 0, 1.0)
	dh.add_item(200, engine)
	dh.update_ship_component(2, 'engine_id', 200)
	
	initial_health = dh.Items[200]['health']
	
	# Attack the engine component
	actions.queue_action(1, 'attack_ship_component', 2, 'engine_id')
	stats = actions.process_tick()
	
	assert stats['attack_ship_component'] == 1
	assert dh.Items[200]['health'] == initial_health - 15.0

def test_collect_item():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with cargo
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	cargo = Cargo(100, 'cargo bay', 0, 10.0)
	dh.add_item(100, cargo)
	dh.update_ship_component(1, 'cargo_id', 100)
	
	# Create item at location
	item = Weapon(200, 'dropped laser', 0, 1.0)
	dh.add_item(200, item)
	dh.add_item_to_location('earth', 200)
	
	# Collect the item
	actions.queue_action(1, 'collect', 200)
	stats = actions.process_tick()
	
	assert stats['collects'] == 1
	assert 200 in dh.Ships[1]['items']
	assert 200 not in dh.Locations['earth']['items']

def test_attack_item_at_location():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	weapon = Weapon(100, 'laser', 0, 20.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	# Create item at location
	target_item = Cargo(200, 'cargo container', 0, 1.0)
	dh.add_item(200, target_item)
	dh.add_item_to_location('earth', 200)
	
	initial_health = dh.Items[200]['health']
	
	# Attack the item
	actions.queue_action(1, 'attack_item', 200)
	stats = actions.process_tick()
	
	assert stats['attack_item'] == 1
	assert dh.Items[200]['health'] == initial_health - 20.0

def test_equip_item_to_ship():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add weapon to cargo
	weapon = Weapon(100, 'laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.add_item_to_ship_cargo(1, 100)
	
	# Equip the weapon
	dh.equip_item_to_ship(1, 100)
	
	assert dh.Ships[1]['weapon_id'] == 100
	assert 100 not in dh.Ships[1]['items']

def test_unequip_item_from_ship():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Equip weapon directly
	weapon = Weapon(100, 'laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.update_ship_component(1, 'weapon_id', 100)
	
	# Unequip the weapon
	dh.unequip_item_from_ship(1, 'weapon_id')
	
	assert dh.Ships[1]['weapon_id'] is None
	assert 100 in dh.Ships[1]['items']

def test_transfer_item_location_to_ship():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add item to location
	weapon = Weapon(100, 'laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.add_item_to_location('earth', 100)
	
	# Transfer to ship
	dh.transfer_item_location_to_ship(100, 'earth', 1)
	
	assert 100 not in dh.Locations['earth']['items']
	assert 100 in dh.Ships[1]['items']

def test_component_repair():
	dh = DataHandler(data_dir="test_data")
	setup_test_handler(dh)
	
	# Create damaged weapon - use tier 1 so multiplier can vary (min=1, max=2)
	weapon = Weapon(100, 'laser', 1, 2.0)
	dh.add_item(100, weapon)
	# Weapon tier 1 health = 50 * (1 + 1) = 100, so 50 = 50%
	dh.set_item_health(100, 50)
	
	# Repair the weapon
	result = components.repair_component(100)
	
	assert result['health_restored'] == 50.0
	assert result['multiplier_reduction'] == 0.05  # 50% health = 0.05 reduction
	assert dh.Items[100]['health'] == 100.0
	assert dh.Items[100]['multiplier'] == 2.0 - 0.05

def test_ship_hp_repair():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	dh.set_ship_hp(1, 50)
	
	# Repair ship
	hp_restored = components.repair_ship_hp(1)
	
	assert hp_restored == 50.0
	assert dh.Ships[1]['hp'] == 100.0

def test_shield_refill():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add shield component
	shield = Shield(100, 'basic shield', 0, 1.0)
	dh.add_item(100, shield)
	dh.update_ship_component(1, 'shield_id', 100)
	dh.set_ship_shield_pool(1, 25.0)
	
	# Refill shields
	shields_restored = components.refill_shield_pool(1)
	max_shield = components.get_ship_max_shield_pool(1)
	
	assert shields_restored == max_shield - 25.0
	assert dh.Ships[1]['shield_pool'] == max_shield

def test_cargo_weight_calculation():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add multiple items to cargo
	weapon1 = Weapon(100, 'laser1', 0, 1.0)  # weight = 10
	weapon2 = Weapon(101, 'laser2', 0, 1.0)  # weight = 10
	dh.add_item(100, weapon1)
	dh.add_item(101, weapon2)
	dh.add_item_to_ship_cargo(1, 100)
	dh.add_item_to_ship_cargo(1, 101)
	
	total_weight = components.get_ship_total_cargo_weight(1)
	assert total_weight == 20.0

def test_can_fit_item_in_cargo():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add cargo with capacity 100
	cargo = Cargo(100, 'cargo bay', 0, 1.0)
	dh.add_item(100, cargo)
	dh.update_ship_component(1, 'cargo_id', 100)
	
	# Add heavy item
	heavy_item = Engine(200, 'heavy engine', 1, 1.0)  # weight = 80
	dh.add_item(200, heavy_item)
	
	# Should fit
	assert components.can_fit_item_in_cargo(1, 200) == True
	
	# Add it to cargo
	dh.add_item_to_ship_cargo(1, 200)
	
	# Create another heavy item
	heavy_item2 = Engine(201, 'another engine', 1, 1.0)  # weight = 80
	dh.add_item(201, heavy_item2)
	
	# Should not fit (80 + 80 > 100)
	assert components.can_fit_item_in_cargo(1, 201) == False

def test_max_hp_calculation():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Tier 0 ship
	ship0 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship0)
	
	# Tier 1 ship - set tier BEFORE creating ship dict
	ship1 = Ship(location='earth')
	ship1['tier'] = 1
	dh.add_ship(2, 'earth', ship1)
	
	max_hp_0 = components.get_ship_max_hp(1)
	max_hp_1 = components.get_ship_max_hp(2)
	
	assert max_hp_0 == 100.0  # 100 * (1 + 0)^2
	assert max_hp_1 == 400.0  # 100 * (1 + 1)^2

def test_shield_pool_max_calculation():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Add tier 0 shield with 2.0 multiplier
	shield = Shield(100, 'shield', 0, 2.0)
	dh.add_item(100, shield)
	dh.update_ship_component(1, 'shield_id', 100)
	
	max_shield = components.get_ship_max_shield_pool(1)
	# 50 * (1 + 0)^1.5 * 2.0 = 100.0
	assert max_shield == 100.0

def test_multiple_ships_same_location_combat():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create 3 ships at earth
	for i in range(1, 4):
		ship = Ship(location='earth')
		dh.add_ship(i, 'earth', ship)
		weapon = Weapon(100 + i, 'laser', 0, 10.0)
		dh.add_item(100 + i, weapon)
		dh.update_ship_component(i, 'weapon_id', 100 + i)
	
	# Ship 1 attacks ship 2, ship 3 attacks ship 1
	actions.queue_action(1, 'attack_ship', 2)
	actions.queue_action(3, 'attack_ship', 1)
	stats = actions.process_tick()
	
	assert stats['attack_ship'] == 2
	assert dh.Ships[2]['hp'] == 90.0
	assert dh.Ships[1]['hp'] == 90.0

def test_action_queue_replacement():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	setup_test_handler(dh)
	
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Queue move to mars
	actions.queue_action(1, 'move', 'mars')
	assert actions.ship_to_node[1].action_type == 'move'
	assert actions.ship_to_node[1].target == 'mars'
	
	# Replace with different move (should update)
	dh.add_location('jupiter')
	dh.double_link_locations('earth', 'jupiter')
	actions.queue_action(1, 'move', 'jupiter')
	assert actions.ship_to_node[1].target == 'jupiter'
	
	# Process tick - should go to jupiter, not mars
	actions.process_tick()
	assert dh.Ships[1]['location'] == 'jupiter'

def test_faction_creation():
	dh = DataHandler(data_dir="test_data")
	
	faction = Faction()
	dh.add_faction(1, faction)
	
	assert 1 in dh.Factions
	assert 'player_ids' in dh.Factions[1]

def test_add_player_to_faction():
	dh = DataHandler(data_dir="test_data")
	
	faction = Faction()
	dh.add_faction(1, faction)
	
	player = Player('test', 1)
	dh.add_player(1, player)
	
	dh.add_player_to_faction(1, 1)
	
	assert 1 in dh.Factions[1]['player_ids']

def test_component_destroyed_at_zero_health():
	dh = DataHandler(data_dir="test_data")
	
	weapon = Weapon(100, 'laser', 0, 5.0)
	dh.add_item(100, weapon)
	
	# Damage to zero
	result = dh.damage_item(100, 999)
	
	assert result['destroyed'] == True
	assert dh.Items[100]['health'] == 0.0
	assert dh.Items[100]['multiplier'] == 0.0

def test_can_equip_item_tier_restriction():
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Tier 0 ship
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Tier 2 weapon
	weapon = Weapon(100, 'advanced laser', 2, 5.0)
	dh.add_item(100, weapon)
	
	# Tier 0 ship can equip tier 2 (tier + 2)
	assert components.can_equip_item(1, 100) == True
	
	# Tier 3 weapon
	weapon2 = Weapon(101, 'super laser', 3, 5.0)
	dh.add_item(101, weapon2)
	
	# Tier 0 ship cannot equip tier 3
	assert components.can_equip_item(1, 101) == False
