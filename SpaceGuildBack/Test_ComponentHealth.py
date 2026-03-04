# Test_ComponentHealth.py
# Tests for component health requirements and combat mechanics
# Created: 25 Feb 2026

from data import DataHandler
from location import Location
from ship import Ship
from item import Weapon, Cargo, Engine, Shield, Sensor, StealthCloak
import components
import actions
import program


def setup_test_handler(dh):
	"""Helper to set up data handler for components and actions modules"""
	program.data_handler = dh
	components.data_handler = dh
	actions.data_handler = dh
	actions.clear_queues()


# ============================================================================
# WEAPON HEALTH = 0 PREVENTS ATTACKS
# ============================================================================

def test_weapon_destroyed_prevents_attack_ship():
	"""Ship with destroyed weapon (health = 0) cannot attack ships"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with destroyed weapon
	ship1 = Ship(location='earth') # create ship
	dh.add_ship(1, 'earth', ship1) # add it to earth
	weapon = Weapon(100, 'broken laser', 0, 5.0) # create weapon item
	dh.add_item(100, weapon) # add to the item dict
	dh.set_item_health(100, 0.0)  # set the item health to zero (TESTING ONLY)
	dh.set_ship_component(1, 'weapon_id', 100) # equip the itme.
	
	# Create target
	ship2 = Ship(location='earth') # create it
	dh.add_ship(2, 'earth', ship2) # add it to earth
	initial_hp = dh.Ships[2]['hp'] # default... hp?
	
	# Queue and process attack - should fail due to destroyed weapon
	actions.queue_action(1, 'attack_ship', 2)
	stats = actions.process_tick()
	
	assert stats['attack_ship'] == 0  # Attack should not process
	assert dh.Ships[2]['hp'] == initial_hp  # Target should be undamaged


def test_weapon_destroyed_prevents_attack_component():
	"""Ship with destroyed weapon (health = 0) cannot attack components"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with destroyed weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'broken laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.set_item_health(100, 0.0)  # Destroyed weapon (TESTING ONLY)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create target with engine
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	engine = Engine(200, 'engine', 0, 1.0)
	dh.add_item(200, engine)
	dh.set_ship_component(2, 'engine_id', 200)
	initial_engine_health = dh.Items[200]['health']
	
	# Queue and process component attack
	actions.queue_action(1, 'attack_ship_component', 2, 'engine_id')
	stats = actions.process_tick()
	
	assert stats['attack_ship_component'] == 0  # Attack should not process
	assert dh.Items[200]['health'] == initial_engine_health  # Engine undamaged


def test_weapon_destroyed_prevents_attack_item():
	"""Ship with destroyed weapon (health = 0) cannot attack items"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with destroyed weapon
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	weapon = Weapon(100, 'broken laser', 0, 5.0)
	dh.add_item(100, weapon)
	dh.set_item_health(100, 0.0)  # Destroyed weapon (TESTING ONLY)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create item at location
	target_item = Cargo(200, 'cargo', 0, 1.0)
	dh.add_item(200, target_item)
	dh.add_item_to_location('earth', 200)
	initial_health = dh.Items[200]['health']
	
	# Queue and process item attack
	actions.queue_action(1, 'attack_item', 200)
	stats = actions.process_tick()
	
	assert stats['attack_item'] == 0  # Attack should not process
	assert dh.Items[200]['health'] == initial_health  # Item undamaged


def test_no_weapon_equipped_prevents_attack():
	"""Ship with no weapon equipped cannot attack"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with NO weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	
	# Create target
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	initial_hp = dh.Ships[2]['hp']
	
	# Queue and process attack
	actions.queue_action(1, 'attack_ship', 2)
	stats = actions.process_tick()
	
	assert stats['attack_ship'] == 0
	assert dh.Ships[2]['hp'] == initial_hp


# ============================================================================
# ENGINE HEALTH = 0 PREVENTS MOVEMENT
# ============================================================================

def test_engine_destroyed_prevents_movement():
	"""Ship with destroyed engine (health = 0) cannot move"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	setup_test_handler(dh)
	
	# Create ship with destroyed engine
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	engine = Engine(100, 'broken engine', 0, 1.0)
	dh.add_item(100, engine)
	dh.set_item_health(100, 0.0)  # Destroyed engine (TESTING ONLY)
	dh.set_ship_component(1, 'engine_id', 100)
	
	# Queue and process move
	actions.queue_action(1, 'move', 'mars')
	stats = actions.process_tick()
	
	assert stats['moves'] == 0  # Move should not process
	assert dh.Ships[1]['location'] == 'earth'  # Ship should stay at earth


def test_no_engine_equipped_prevents_movement():
	"""Ship with no engine equipped cannot move"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	dh.add_location('mars')
	dh.double_link_locations('earth', 'mars')
	setup_test_handler(dh)
	
	# Create ship with NO engine
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Queue and process move
	actions.queue_action(1, 'move', 'mars')
	stats = actions.process_tick()
	
	assert stats['moves'] == 0
	assert dh.Ships[1]['location'] == 'earth'


# ============================================================================
# SENSOR HEALTH = 0 PREVENTS SCANS
# ============================================================================

def test_sensor_destroyed_prevents_ship_scan():
	"""Ship with destroyed sensor (health = 0) cannot scan ships"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create scanner with destroyed sensor
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	sensor = Sensor(100, 'broken sensor', 0, 1.0)
	dh.add_item(100, sensor)
	dh.set_item_health(100, 0.0)  # Destroyed sensor (TESTING ONLY)
	dh.set_ship_component(1, 'sensor_id', 100)
	
	# Create target
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	
	# Try to scan - should return None (failed)
	result = actions.scan_ship(1, 2)
	assert result is None


def test_sensor_destroyed_prevents_item_scan():
	"""Ship with destroyed sensor (health = 0) cannot scan items"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create scanner with destroyed sensor
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	sensor = Sensor(100, 'broken sensor', 0, 1.0)
	dh.add_item(100, sensor)
	dh.set_item_health(100, 0.0)  # Destroyed sensor (TESTING ONLY)
	dh.set_ship_component(1, 'sensor_id', 100)
	
	# Create item at location
	item = Weapon(200, 'laser', 0, 1.0)
	dh.add_item(200, item)
	dh.add_item_to_location('earth', 200)
	
	# Try to scan - should return None (failed)
	result = actions.scan_item(1, 200)
	assert result is None


def test_sensor_destroyed_prevents_location_scan():
	"""Ship with destroyed sensor (health = 0) cannot scan locations"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create scanner with destroyed sensor
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	sensor = Sensor(100, 'broken sensor', 0, 1.0)
	dh.add_item(100, sensor)
	dh.set_item_health(100, 0.0)  # Destroyed sensor (TESTING ONLY)
	dh.set_ship_component(1, 'sensor_id', 100)
	
	# Try to scan location - should return None (failed)
	result = actions.scan_location(1, 'earth')
	assert result is None


def test_no_sensor_equipped_prevents_scan():
	"""Ship with no sensor equipped cannot scan"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create scanner with NO sensor
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	
	# Create target
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	
	# Try to scan - should fail
	result = actions.scan_ship(1, 2)
	assert result is None


# ============================================================================
# CARGO HEALTH = 0 PREVENTS PICKUP
# ============================================================================

def test_cargo_destroyed_prevents_collection():
	"""Ship with destroyed cargo (health = 0) cannot collect items"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with destroyed cargo
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	cargo = Cargo(100, 'broken cargo', 0, 1.0)
	dh.add_item(100, cargo)
	dh.set_item_health(100, 0.0)  # Destroyed cargo (TESTING ONLY)
	dh.set_ship_component(1, 'cargo_id', 100)
	
	# Create item at location
	item = Weapon(200, 'laser', 0, 1.0)
	dh.add_item(200, item)
	dh.add_item_to_location('earth', 200)
	
	# Queue and process collection
	actions.queue_action(1, 'collect', 200)
	stats = actions.process_tick()
	
	assert stats['collects'] == 0  # Collect should not process
	assert 200 not in dh.Ships[1]['items']  # Item not collected
	assert 200 in dh.Locations['earth']['items']  # Item still at location


def test_no_cargo_equipped_prevents_collection():
	"""Ship with no cargo equipped cannot collect items"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with NO cargo
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	
	# Create item at location
	item = Weapon(200, 'laser', 0, 1.0)
	dh.add_item(200, item)
	dh.add_item_to_location('earth', 200)
	
	# Queue and process collection
	actions.queue_action(1, 'collect', 200)
	stats = actions.process_tick()
	
	assert stats['collects'] == 0
	assert 200 not in dh.Ships[1]['items']
	assert 200 in dh.Locations['earth']['items']


# ============================================================================
# SHIELD DESTRUCTION CLEARS POOL
# ============================================================================

def test_shield_destroyed_clears_pool():
	"""When shield is destroyed (health = 0), shield pool auto-clears to 0"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with shield and pool
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	shield = Shield(100, 'shield', 0, 1.0)
	dh.add_item(100, shield)
	dh.set_ship_component(1, 'shield_id', 100)
	dh.set_ship_shield_pool(1, 50.0)
	
	# Verify shield pool is set
	assert dh.Ships[1]['shield_pool'] == 50.0
	
	# Destroy the shield component
	dh.damage_item(100, 999)
	
	# Shield pool should auto-clear to 0
	assert dh.Ships[1]['shield_pool'] == 0.0


def test_shield_unequipped_clears_pool():
	"""When shield is unequipped, shield pool auto-clears to 0"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with shield and pool
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	shield = Shield(100, 'shield', 0, 1.0)
	dh.add_item(100, shield)
	dh.set_ship_component(1, 'shield_id', 100)
	dh.set_ship_shield_pool(1, 50.0)
	
	# Verify shield pool is set
	assert dh.Ships[1]['shield_pool'] == 50.0
	
	# Unequip the shield
	dh.unequip_item_from_ship(1, 'shield_id')
	
	# Shield pool should auto-clear to 0
	assert dh.Ships[1]['shield_pool'] == 0.0


# ============================================================================
# EMPTY SLOT CRITICAL DAMAGE
# ============================================================================

def test_empty_weapon_slot_takes_critical_damage_when_shields_down():
	"""Attacking empty weapon slot deals 5x damage to ship HP when shields down"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 10.0)
	dh.add_item(100, weapon)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create target with NO weapon and NO shields
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	initial_hp = dh.Ships[2]['hp']
	
	# Attack empty weapon slot
	actions.queue_action(1, 'attack_ship_component', 2, 'weapon_id')
	stats = actions.process_tick()
	
	assert stats['attack_ship_component'] == 1
	# Should deal 10 * 5 = 50 damage to ship HP
	assert dh.Ships[2]['hp'] == initial_hp - 50.0


def test_empty_slot_with_shields_takes_normal_damage():
	"""Attacking empty slot with shields up deals normal damage to shields"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 10.0)
	dh.add_item(100, weapon)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create target with NO weapon but WITH shields
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	shield = Shield(200, 'shield', 0, 1.0)
	dh.add_item(200, shield)
	dh.set_ship_component(2, 'shield_id', 200)
	dh.set_ship_shield_pool(2, 100.0)
	initial_hp = dh.Ships[2]['hp']
	
	# Attack empty weapon slot
	actions.queue_action(1, 'attack_ship_component', 2, 'weapon_id')
	stats = actions.process_tick()
	
	assert stats['attack_ship_component'] == 1
	# Should deal normal 10 damage to shields, not critical
	assert dh.Ships[2]['shield_pool'] == 90.0
	assert dh.Ships[2]['hp'] == initial_hp  # HP should be untouched


def test_multiple_empty_slots_critical_damage():
	"""Test critical damage on different empty component slots"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon (20 damage)
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 20.0)
	dh.add_item(100, weapon)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create target with NO components and NO shields
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	initial_hp = dh.Ships[2]['hp']
	
	# Attack empty engine slot - should deal 5x damage
	actions.queue_action(1, 'attack_ship_component', 2, 'engine_id')
	actions.process_tick()
	
	assert dh.Ships[2]['hp'] == initial_hp - 100.0  # 20 * 5 = 100
	
	# Reset and attack empty sensor slot
	dh.set_ship_hp(2, initial_hp)
	actions.clear_queues()
	
	actions.queue_action(1, 'attack_ship_component', 2, 'sensor')
	actions.process_tick()
	
	assert dh.Ships[2]['hp'] == initial_hp - 100.0  # 20 * 5 = 100


# ============================================================================
# CARGO DESTRUCTION SPILLAGE
# ============================================================================

def test_cargo_destroyed_spills_items_to_location():
	"""When cargo is destroyed, all items spill to current location"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with cargo holding multiple items
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	cargo = Cargo(100, 'cargo bay', 0, 1.0)
	dh.add_item(100, cargo)
	dh.set_ship_component(1, 'cargo_id', 100)
	
	# Add items to cargo
	item1 = Weapon(200, 'laser1', 0, 1.0)
	item2 = Weapon(201, 'laser2', 0, 1.0)
	item3 = Engine(202, 'engine', 0, 1.0)
	dh.add_item(200, item1)
	dh.add_item(201, item2)
	dh.add_item(202, item3)
	dh.add_item_to_ship_cargo(1, 200)
	dh.add_item_to_ship_cargo(1, 201)
	dh.add_item_to_ship_cargo(1, 202)
	
	# Verify items are in cargo
	assert 200 in dh.Ships[1]['items']
	assert 201 in dh.Ships[1]['items']
	assert 202 in dh.Ships[1]['items']
	assert 200 not in dh.Locations['earth']['items']
	
	# Destroy the cargo component
	dh.damage_item(100, 999)
	
	# Items should have spilled to location
	assert 200 not in dh.Ships[1]['items']
	assert 201 not in dh.Ships[1]['items']
	assert 202 not in dh.Ships[1]['items']
	assert 200 in dh.Locations['earth']['items']
	assert 201 in dh.Locations['earth']['items']
	assert 202 in dh.Locations['earth']['items']


def test_cargo_destroyed_in_combat_spills_items():
	"""When cargo is destroyed via combat, items spill to location"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create attacker with weapon
	ship1 = Ship(location='earth')
	dh.add_ship(1, 'earth', ship1)
	weapon = Weapon(100, 'laser', 0, 999.0)  # High damage
	dh.add_item(100, weapon)
	dh.set_ship_component(1, 'weapon_id', 100)
	
	# Create target with cargo holding items
	ship2 = Ship(location='earth')
	dh.add_ship(2, 'earth', ship2)
	cargo = Cargo(200, 'cargo bay', 0, 1.0)
	dh.add_item(200, cargo)
	dh.set_ship_component(2, 'cargo_id', 200)
	
	# Add item to cargo
	item = Sensor(300, 'sensor', 0, 1.0)
	dh.add_item(300, item)
	dh.add_item_to_ship_cargo(2, 300)
	
	# Verify item is in cargo
	assert 300 in dh.Ships[2]['items']
	assert 300 not in dh.Locations['earth']['items']
	
	# Attack and destroy the cargo
	actions.queue_action(1, 'attack_ship_component', 2, 'cargo_id')
	actions.process_tick()
	
	# Item should have spilled to location
	assert 300 not in dh.Ships[2]['items']
	assert 300 in dh.Locations['earth']['items']


def test_empty_cargo_destroyed_no_spillage():
	"""Destroying empty cargo should not cause errors"""
	dh = DataHandler(data_dir="test_data")
	dh.add_location('earth')
	setup_test_handler(dh)
	
	# Create ship with empty cargo
	ship = Ship(location='earth')
	dh.add_ship(1, 'earth', ship)
	cargo = Cargo(100, 'cargo bay', 0, 1.0)
	dh.add_item(100, cargo)
	dh.set_ship_component(1, 'cargo_id', 100)
	
	# Verify cargo is empty
	assert len(dh.Ships[1]['items']) == 0
	
	# Destroy the cargo - should not error
	dh.damage_item(100, 999)
	
	# Location should still have no items
	assert len(dh.Locations['earth']['items']) == 0
