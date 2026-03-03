# Test to verify action results accumulate properly across multiple ticks
# This tests the fix for the bug where existing action results would prevent
# new results from being written.

from actions import (
    add_scan_result,
    add_attack_result,
    add_move_result,
    add_collect_result,
    get_and_clear_action_results,
    action_results,
    action_results_locks
)


def test_action_results_accumulate_across_ticks():
    """Test that action results can accumulate if client doesn't retrieve them.
    
    This simulates the "early return" scenario where a ship has action results
    from tick 1, but before the client retrieves them, tick 2 processes and
    adds more results. The new results should be written, not skipped.
    """
    # Clear state
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 100
    
    # Tick 1: Ship performs a scan
    add_scan_result(ship_id, {"scan_type": "ship", "target": 1, "tick": 1})
    
    # Verify tick 1 result exists
    assert ship_id in action_results
    assert action_results[ship_id]["scan_data"]["tick"] == 1
    assert action_results[ship_id]["attack_result"] is None
    
    # Tick 2: Before client retrieves results, ship performs an attack
    # This should NOT skip writing because ship_id is already in action_results
    add_attack_result(ship_id, {"attack_type": "ship", "target": 2, "tick": 2})
    
    # Verify BOTH results exist
    assert action_results[ship_id]["scan_data"]["tick"] == 1  # Old result preserved
    assert action_results[ship_id]["attack_result"]["tick"] == 2  # New result added
    
    # Tick 3: Ship performs move and collect
    add_move_result(ship_id, {"destination": "Mars", "tick": 3})
    add_collect_result(ship_id, {"item_id": 999, "tick": 3})
    
    # Verify ALL results accumulated
    assert action_results[ship_id]["scan_data"]["tick"] == 1
    assert action_results[ship_id]["attack_result"]["tick"] == 2
    assert action_results[ship_id]["move_result"]["tick"] == 3
    assert action_results[ship_id]["collect_result"]["tick"] == 3
    
    # Client finally retrieves all accumulated results
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    assert results["scan_data"]["tick"] == 1
    assert results["attack_result"]["tick"] == 2
    assert results["move_result"]["tick"] == 3
    assert results["collect_result"]["tick"] == 3
    
    # Verify cleaned up
    assert ship_id not in action_results
    
    print("[PASS] Action results accumulate correctly across ticks")


def test_action_results_can_overwrite_same_type():
    """Test that writing the same result type multiple times overwrites.
    
    If a ship scans twice before client retrieves, the second scan should
    overwrite the first (latest data wins).
    """
    # Clear state
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 200
    
    # First scan
    add_scan_result(ship_id, {"scan_type": "ship", "target": 1, "data": "old"})
    assert action_results[ship_id]["scan_data"]["data"] == "old"
    
    # Second scan (should overwrite)
    add_scan_result(ship_id, {"scan_type": "ship", "target": 2, "data": "new"})
    assert action_results[ship_id]["scan_data"]["data"] == "new"
    assert action_results[ship_id]["scan_data"]["target"] == 2
    
    # First attack
    add_attack_result(ship_id, {"attack_type": "ship", "damage": 10})
    assert action_results[ship_id]["attack_result"]["damage"] == 10
    
    # Second attack (should overwrite)
    add_attack_result(ship_id, {"attack_type": "component", "damage": 20})
    assert action_results[ship_id]["attack_result"]["damage"] == 20
    assert action_results[ship_id]["attack_result"]["attack_type"] == "component"
    
    # Scan should still be preserved (only attack overwrote)
    assert action_results[ship_id]["scan_data"]["data"] == "new"
    
    print("[PASS] Action results overwrite correctly for same type")


def test_setdefault_preserves_existing_structure():
    """Test that _ensure_action_results doesn't overwrite existing data.
    
    This verifies that setdefault is working correctly - it should only
    create the dict if it doesn't exist, not overwrite existing keys.
    """
    # Clear state
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 300
    
    # Add scan result
    add_scan_result(ship_id, {"target": 1})
    
    # Manually verify the structure
    assert "scan_data" in action_results[ship_id]
    assert "attack_result" in action_results[ship_id]
    assert action_results[ship_id]["scan_data"]["target"] == 1
    assert action_results[ship_id]["attack_result"] is None
    
    # Add attack result (this calls _ensure_action_results again)
    add_attack_result(ship_id, {"damage": 50})
    
    # Scan should still be there (setdefault didn't overwrite)
    assert action_results[ship_id]["scan_data"]["target"] == 1
    assert action_results[ship_id]["attack_result"]["damage"] == 50
    
    print("[PASS] setdefault preserves existing structure")


if __name__ == "__main__":
    test_action_results_accumulate_across_ticks()
    test_action_results_can_overwrite_same_type()
    test_setdefault_preserves_existing_structure()
    print("\n[PASS] All action results accumulation tests passed!")
