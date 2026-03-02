# Aidan Orion 2 Mar 2026
# Integration test for spawn_ship() and spawn_item() methods

from data import DataHandler
from ship import Ship
from item import Engine, Weapon, Cargo

def test_spawn_methods():
    """Test that spawn_ship() and spawn_item() work correctly with DataHandler."""
    
    print("\n[Integration Test] Testing spawn methods with DataHandler")
    
    # Create DataHandler with test directory
    dh = DataHandler(data_dir="test_spawn_data", create_dir=True)
    
    # Add a test location
    dh.add_location("test_location", location_type="space")
    
    # Initialize ID generator (normally called after load_all)
    dh.initialize_id_generator()
    
    # Test spawn_ship()
    print("\n[Test 1] Spawning ships with auto-generated IDs...")
    ship1 = dh.spawn_ship("test_location", Ship(location="test_location"))
    ship2 = dh.spawn_ship("test_location", Ship(location="test_location"))
    ship3 = dh.spawn_ship("test_location", Ship(location="test_location"))
    
    print(f"  Ship 1 ID: {ship1['id']}")
    print(f"  Ship 2 ID: {ship2['id']}")
    print(f"  Ship 3 ID: {ship3['id']}")
    
    # Verify IDs are unique
    assert ship1['id'] != ship2['id']
    assert ship2['id'] != ship3['id']
    assert ship1['id'] != ship3['id']
    print("  [OK] All ship IDs are unique")
    
    # Verify ships are in DataHandler
    assert ship1['id'] in dh.Ships
    assert ship2['id'] in dh.Ships
    assert ship3['id'] in dh.Ships
    print("  [OK] All ships added to DataHandler.Ships")
    
    # Verify ships are in location
    assert ship1['id'] in dh.Locations['test_location']['ship_ids']
    assert ship2['id'] in dh.Locations['test_location']['ship_ids']
    assert ship3['id'] in dh.Locations['test_location']['ship_ids']
    print("  [OK] All ships added to location")
    
    # Test spawn_item()
    print("\n[Test 2] Spawning items with auto-generated IDs...")
    # Note: The old ID parameter will be overwritten by spawn_item()
    item1 = dh.spawn_item(Engine(ID_=0, name_="Test Engine", tier_=0, mult_=1.0))
    item2 = dh.spawn_item(Weapon(ID_=0, name_="Test Weapon", tier_=1, mult_=1.5))
    item3 = dh.spawn_item(Cargo(ID_=0, name_="Test Cargo", tier_=2, mult_=2.0))
    
    print(f"  Item 1 ID: {item1['id']}")
    print(f"  Item 2 ID: {item2['id']}")
    print(f"  Item 3 ID: {item3['id']}")
    
    # Verify IDs are unique
    assert item1['id'] != item2['id']
    assert item2['id'] != item3['id']
    assert item1['id'] != item3['id']
    print("  [OK] All item IDs are unique")
    
    # Verify items are in DataHandler
    assert item1['id'] in dh.Items
    assert item2['id'] in dh.Items
    assert item3['id'] in dh.Items
    print("  [OK] All items added to DataHandler.Items")
    
    # Verify ship and item IDs don't overlap
    all_ids = [ship1['id'], ship2['id'], ship3['id'], item1['id'], item2['id'], item3['id']]
    assert len(all_ids) == len(set(all_ids))
    print("  [OK] Ship and item IDs don't overlap")
    
    # Test recovery after simulated restart
    print("\n[Test 3] Testing ID recovery after restart...")
    existing_ids = list(dh.Ships.keys()) + list(dh.Items.keys())
    
    # Create new DataHandler and reinitialize with existing IDs
    dh2 = DataHandler(data_dir="test_spawn_data_2", create_dir=True)
    dh2.add_location("test_location", location_type="space")
    
    # Manually add existing entities to simulate loading from save
    for ship_id in dh.Ships.keys():
        dh2.Ships[ship_id] = dh.Ships[ship_id]
    for item_id in dh.Items.keys():
        dh2.Items[item_id] = dh.Items[item_id]
    
    # Initialize ID generator with existing IDs
    dh2.initialize_id_generator()
    
    # Generate new IDs
    new_ship = dh2.spawn_ship("test_location", Ship(location="test_location"))
    new_item = dh2.spawn_item(Engine(ID_=0, name_="New Engine", tier_=0, mult_=1.0))
    
    print(f"  New ship ID after restart: {new_ship['id']}")
    print(f"  New item ID after restart: {new_item['id']}")
    
    # Verify no duplicates
    assert new_ship['id'] not in existing_ids
    assert new_item['id'] not in existing_ids
    print("  [OK] No duplicate IDs after restart")
    
    print("\n[Integration Test] [OK] All tests passed!")
    print(f"\nGenerated {len(all_ids) + 2} unique IDs across ships and items")
    
    # Cleanup
    import shutil
    import os
    if os.path.exists("test_spawn_data"):
        shutil.rmtree("test_spawn_data")
    if os.path.exists("test_spawn_data_2"):
        shutil.rmtree("test_spawn_data_2")


if __name__ == "__main__":
    test_spawn_methods()
