"""Test script for safe zone mechanics.

This script tests the safe zone functionality without any file I/O.
All data is kept in memory only.
"""

from data import DataHandler
from actions import _set_data_handler, is_safe_zone
from setup import create_world_locations, create_world_links


def setup_test_world():
    """Create a test world in memory without any file I/O.
    
    Returns:
        DataHandler instance with all locations loaded in memory
    """
    # Create DataHandler with no directory creation
    dh = DataHandler(data_dir="__test_data__", create_dir=False)
    
    # Get location data from setup functions
    location_metadata = create_world_locations()
    bidirectional_links, single_links = create_world_links()
    
    # Create all locations in memory
    for location_name, metadata in location_metadata.items():
        dh.add_location(
            location_name,
            location_type=metadata.get('type', 'space'),
            controlled_by=metadata.get('controlled_by', 'ORION'),
            description=metadata.get('description', ''),
            tags=metadata.get('tags', []),
            spawnable_ids=metadata.get('spawnable_ids', []),
            resource_node_ids=metadata.get('resource_node_ids', [])
        )
    
    # Create bidirectional links
    for loc1, loc2 in bidirectional_links:
        dh.double_link_locations(loc1, loc2)
    
    # Create single-directional links
    for source, dest, _ in single_links:
        dh.single_link_locations(source, dest)
    
    # DO NOT call dh.save_all() - keep everything in memory only
    
    return dh


def run_tests():
    """Run all safe zone tests."""
    print('=' * 70)
    print('SAFE ZONE MECHANICS TEST')
    print('=' * 70)
    
    print('\n[*] Setting up test world (in-memory only, no file I/O)...')
    dh = setup_test_world()
    
    # Set the data handler for actions module
    print('[*] Injecting DataHandler into actions module...')
    _set_data_handler(dh)
    
    print('\n[*] Running safe zone detection tests...\n')
    
    # Test safe zone (station)
    is_safe = is_safe_zone('Earth_Orbital_Station_Zero')
    print(f'[TEST 1] Earth_Orbital_Station_Zero is safe zone: {is_safe}')
    assert is_safe == True, f"Expected Earth_Orbital_Station_Zero to be a safe zone! Got {is_safe}"
    
    # Test another safe zone (space location)
    is_safe2 = is_safe_zone('Earth_Orbit')
    print(f'[TEST 2] Earth_Orbit is safe zone: {is_safe2}')
    assert is_safe2 == True, f"Expected Earth_Orbit to be a safe zone! Got {is_safe2}"
    
    # Test dangerous zone
    is_dangerous = is_safe_zone('KR1_Resource_1')
    print(f'[TEST 3] KR1_Resource_1 is safe zone: {is_dangerous}')
    assert is_dangerous == False, f"Expected KR1_Resource_1 to NOT be a safe zone! Got {is_dangerous}"
    
    # Test enforced zone (should NOT be safe - only 'Safe' tag disables weapons)
    is_enforced = is_safe_zone('Sun_Orbit')
    print(f'[TEST 4] Sun_Orbit (Enforced) is safe zone: {is_enforced}')
    assert is_enforced == False, f"Expected Sun_Orbit (Enforced) to NOT be a safe zone! Got {is_enforced}"
    
    # Test patrolled zone (should NOT be safe)
    is_patrolled = is_safe_zone('Asteroid_Belt_Region_1')
    print(f'[TEST 5] Asteroid_Belt_Region_1 (Patrolled) is safe zone: {is_patrolled}')
    assert is_patrolled == False, f"Expected Asteroid_Belt_Region_1 (Patrolled) to NOT be a safe zone! Got {is_patrolled}"
    
    # Test a neutral location
    is_neutral = is_safe_zone('Kuiper_Region_1')
    print(f'[TEST 6] Kuiper_Region_1 (no specific tag) is safe zone: {is_neutral}')
    assert is_neutral == False, f"Expected Kuiper_Region_1 to NOT be a safe zone! Got {is_neutral}"
    
    # Verify location data directly
    print(f'\n[*] Sample location data verification:')
    loc = dh.get_location('Earth_Orbital_Station_Zero')
    print(f'  Safe location: {loc.get("name")} - Tags: {loc.get("tags")}')
    loc2 = dh.get_location('Sun_Orbit')
    print(f'  Enforced location: {loc2.get("name")} - Tags: {loc2.get("tags")}')
    loc3 = dh.get_location('KR1_Resource_1')
    print(f'  Dangerous location: {loc3.get("name")} - Tags: {loc3.get("tags")}')
    
    # Count statistics
    safe_count = sum(1 for loc in dh.Locations.values() if 'Safe' in loc.get('tags', []))
    dangerous_count = sum(1 for loc in dh.Locations.values() if 'Dangerous' in loc.get('tags', []))
    
    print(f'\n[*] World statistics:')
    print(f'  Total locations: {len(dh.Locations)}')
    print(f'  Safe zones (weapons disabled): {safe_count}')
    print(f'  Dangerous zones: {dangerous_count}')
    print(f'  Other zones (weapons enabled): {len(dh.Locations) - safe_count - dangerous_count}')
    
    print('\n' + '=' * 70)
    print('[+] ALL SAFE ZONE TESTS PASSED!')
    print('[+] Safe zone mechanics are working correctly!')
    print('=' * 70)


if __name__ == '__main__':
    run_tests()
