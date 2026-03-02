"""
Test the updates endpoint functionality - action results tracking.
Aidan Orion 2 Mar 2026
"""

from data import DataHandler
from ship import Ship
from item import Weapon, Sensor, Engine
import components
import actions
import program


def setup_test_handler(dh):
    """Helper to set up data handler for components and actions modules"""
    program.data_handler = dh
    components.data_handler = dh
    actions._set_data_handler(dh)
    actions.clear_queues()  # Clear any leftover actions from previous tests


def test_action_results_storage():
    """Test that action results can be stored and retrieved"""
    # Test scan result
    actions.add_scan_result(1, {
        'scan_type': 'ship',
        'target': 2,
        'data': {'hp': 100}
    })
    
    results = actions.get_and_clear_action_results(1)
    assert results is not None
    assert results['scan_data'] is not None
    assert results['scan_data']['scan_type'] == 'ship'
    
    # Verify cleared
    results2 = actions.get_and_clear_action_results(1)
    assert results2 is None
    
    print("[PASS] Action results storage test passed")


def test_multiple_action_results():
    """Test that multiple action results can be stored for the same ship"""
    ship_id = 123
    
    # Add scan result
    actions.add_scan_result(ship_id, {
        'scan_type': 'ship',
        'target': 456,
        'data': {'hp': 100}
    })
    
    # Add attack result  
    actions.add_attack_result(ship_id, {
        'attack_type': 'ship',
        'target_ship_id': 789,
        'success': True
    })
    
    # Add move result
    actions.add_move_result(ship_id, {
        'destination': 'Mars',
        'success': True
    })
    
    # Get all results
    results = actions.get_and_clear_action_results(ship_id)
    assert results is not None
    assert results['scan_data'] is not None
    assert results['attack_result'] is not None
    assert results['move_result'] is not None
    
    print("[PASS] Multiple action results test passed")


if __name__ == '__main__':
    test_action_results_storage()
    test_multiple_action_results()
    print("\n[SUCCESS] All action result tracking tests passed!")
