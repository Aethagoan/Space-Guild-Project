# SpaceGuildBack/test_scan_location_limits.py
# Test that station scans return ship_count instead of ship_ids

import pytest
import actions
import components
import program
from data import DataHandler

def setup_test_handler(dh):
    """Helper to set up data handler for actions and components modules"""
    program.data_handler = dh
    components.data_handler = dh
    actions._set_data_handler(dh)
    actions.clear_queues()

@pytest.fixture
def data_handler():
    """Create a fresh DataHandler for testing."""
    dh = DataHandler(data_dir="test_scan_data", create_dir=True)
    dh.initialize_id_generator()  # Required for spawn_ship/spawn_item
    setup_test_handler(dh)
    return dh


def test_scan_space_location_returns_ship_ids(data_handler):
    """Test that scanning a space location returns full ship_ids list."""
    from ship import Ship
    from item import Sensor
    
    # Create locations
    data_handler.add_location('earth_orbit', location_type='space')
    data_handler.add_location('mars_orbit', location_type='space')
    
    # Create scanner ship at earth with sensor
    scanner_ship_data = Ship(location='earth_orbit')
    scanner_ship = data_handler.spawn_ship('earth_orbit', scanner_ship_data)
    scanner_id = scanner_ship['id']
    
    sensor_data = Sensor(ID_=1, name_='Test Sensor', tier_=1, mult_=1.0)
    sensor = data_handler.spawn_item(sensor_data)
    sensor_id = sensor['id']
    data_handler.set_ship_component(scanner_id, 'sensor_id', sensor_id)
    
    # Create 5 ships at mars
    ship_ids_at_mars = []
    for i in range(5):
        ship_data = Ship(location='mars_orbit')
        ship = data_handler.spawn_ship('mars_orbit', ship_data)
        ship_ids_at_mars.append(ship['id'])
    
    # Scan mars from earth
    result = actions.scan_location(scanner_id, 'mars_orbit')
    
    # Should return full ship_ids list for space location
    assert result is not None
    assert result['location_type'] == 'space'
    assert 'ship_ids' in result
    assert 'ship_count' not in result
    assert len(result['ship_ids']) == 5
    assert set(result['ship_ids']) == set(ship_ids_at_mars)


def test_scan_station_returns_ship_count(data_handler):
    """Test that scanning a station returns ship_count instead of ship_ids."""
    from ship import Ship
    from item import Sensor
    
    # Create locations
    data_handler.add_location('earth_orbit', location_type='space')
    data_handler.add_location('earth_station', location_type='station')
    
    # Create scanner ship at earth with sensor
    scanner_ship_data = Ship(location='earth_orbit')
    scanner_ship = data_handler.spawn_ship('earth_orbit', scanner_ship_data)
    scanner_id = scanner_ship['id']
    
    sensor_data = Sensor(ID_=1, name_='Test Sensor', tier_=1, mult_=1.0)
    sensor = data_handler.spawn_item(sensor_data)
    sensor_id = sensor['id']
    data_handler.set_ship_component(scanner_id, 'sensor_id', sensor_id)
    
    # Create 100 ships at station (simulating crowded station)
    for i in range(100):
        ship_data = Ship(location='earth_station')
        data_handler.spawn_ship('earth_station', ship_data)
    
    # Scan station from earth_orbit
    result = actions.scan_location(scanner_id, 'earth_station')
    
    # Should return ship_count instead of ship_ids for station
    assert result is not None
    assert result['location_type'] == 'station'
    assert 'ship_count' in result
    assert 'ship_ids' not in result
    assert result['ship_count'] == 100


def test_scan_ground_station_returns_ship_count(data_handler):
    """Test that scanning a ground_station also returns ship_count."""
    from ship import Ship
    from item import Sensor
    
    # Create locations
    data_handler.add_location('mars_orbit', location_type='space')
    data_handler.add_location('mars_ground', location_type='ground_station')
    
    # Create scanner ship at mars orbit with sensor
    scanner_ship_data = Ship(location='mars_orbit')
    scanner_ship = data_handler.spawn_ship('mars_orbit', scanner_ship_data)
    scanner_id = scanner_ship['id']
    
    sensor_data = Sensor(ID_=1, name_='Test Sensor', tier_=1, mult_=1.0)
    sensor = data_handler.spawn_item(sensor_data)
    sensor_id = sensor['id']
    data_handler.set_ship_component(scanner_id, 'sensor_id', sensor_id)
    
    # Create 50 ships at ground station
    for i in range(50):
        ship_data = Ship(location='mars_ground')
        data_handler.spawn_ship('mars_ground', ship_data)
    
    # Scan ground station from orbit
    result = actions.scan_location(scanner_id, 'mars_ground')
    
    # Should return ship_count for ground_station too
    assert result is not None
    assert result['location_type'] == 'ground_station'
    assert 'ship_count' in result
    assert 'ship_ids' not in result
    assert result['ship_count'] == 50


def test_scan_resource_node_returns_ship_ids(data_handler):
    """Test that scanning a resource_node returns full ship_ids list."""
    from ship import Ship
    from item import Sensor
    
    # Create locations
    data_handler.add_location('asteroid_belt', location_type='space')
    data_handler.add_location('rich_asteroid', location_type='resource_node')
    
    # Create scanner ship with sensor
    scanner_ship_data = Ship(location='asteroid_belt')
    scanner_ship = data_handler.spawn_ship('asteroid_belt', scanner_ship_data)
    scanner_id = scanner_ship['id']
    
    sensor_data = Sensor(ID_=1, name_='Test Sensor', tier_=1, mult_=1.0)
    sensor = data_handler.spawn_item(sensor_data)
    sensor_id = sensor['id']
    data_handler.set_ship_component(scanner_id, 'sensor_id', sensor_id)
    
    # Create 3 ships at resource node
    ship_ids_at_resource = []
    for i in range(3):
        ship_data = Ship(location='rich_asteroid')
        ship = data_handler.spawn_ship('rich_asteroid', ship_data)
        ship_ids_at_resource.append(ship['id'])
    
    # Scan resource node
    result = actions.scan_location(scanner_id, 'rich_asteroid')
    
    # Should return full ship_ids list for resource_node
    assert result is not None
    assert result['location_type'] == 'resource_node'
    assert 'ship_ids' in result
    assert 'ship_count' not in result
    assert len(result['ship_ids']) == 3


def test_scan_station_filters_stealthed_ships(data_handler):
    """Test that ship_count excludes stealthed ships."""
    from ship import Ship
    from item import Sensor, StealthCloak
    
    # Create locations
    data_handler.add_location('earth_orbit', location_type='space')
    data_handler.add_location('earth_station', location_type='station')
    
    # Create scanner ship with sensor
    scanner_ship_data = Ship(location='earth_orbit')
    scanner_ship = data_handler.spawn_ship('earth_orbit', scanner_ship_data)
    scanner_id = scanner_ship['id']
    
    sensor_data = Sensor(ID_=1, name_='Test Sensor', tier_=1, mult_=1.0)
    sensor = data_handler.spawn_item(sensor_data)
    sensor_id = sensor['id']
    data_handler.set_ship_component(scanner_id, 'sensor_id', sensor_id)
    
    # Create 10 ships at station
    for i in range(10):
        ship_data = Ship(location='earth_station')
        ship = data_handler.spawn_ship('earth_station', ship_data)
        ship_id = ship['id']
        
        # Make 3 of them stealthed
        if i < 3:
            stealth_data = StealthCloak(ID_=100+i, name_='Cloak', tier_=1, mult_=1.0)
            stealth = data_handler.spawn_item(stealth_data)
            stealth_id = stealth['id']
            data_handler.set_ship_component(ship_id, 'stealth_cloak_id', stealth_id)
            actions.activate_stealth(ship_id)
    
    # Scan station
    result = actions.scan_location(scanner_id, 'earth_station')
    
    # Should count only visible ships (10 - 3 stealthed = 7)
    assert result is not None
    assert result['ship_count'] == 7


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
