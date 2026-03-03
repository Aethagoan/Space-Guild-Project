# Test simulating the actual API workflow with early returns
# This tests that action results work correctly when the client
# polls at different intervals than tick processing.

import time
from actions import (
    add_scan_result,
    add_attack_result,
    add_move_result,
    get_and_clear_action_results,
    action_results,
    action_results_locks
)


def test_api_workflow_early_return():
    """Simulate the actual API workflow where client polls every 500ms.
    
    Scenario:
    - Tick 1: Ship scans and attacks
    - Client polls immediately (gets results)
    - Tick 2: Ship moves
    - Tick 3: Ship scans again (before client polls)
    - Client polls (should get results from tick 2 and 3)
    """
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 1000
    
    # === TICK 1 ===
    print("\n[TICK 1] Processing scan and attack")
    add_scan_result(ship_id, {"target": "ship_1", "tick": 1})
    add_attack_result(ship_id, {"target": "ship_1", "tick": 1})
    
    # Client polls immediately
    print("[CLIENT] Polling /updates endpoint")
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    assert results["scan_data"]["tick"] == 1
    assert results["attack_result"]["tick"] == 1
    assert results["move_result"] is None
    print(f"[CLIENT] Got results: scan={results['scan_data']['target']}, attack={results['attack_result']['target']}")
    
    # Results should be cleared
    assert ship_id not in action_results
    
    # === TICK 2 ===
    print("\n[TICK 2] Processing move")
    add_move_result(ship_id, {"destination": "Mars", "tick": 2})
    
    # === TICK 3 ===
    # Client hasn't polled yet, so tick 2 results are still there
    print("[TICK 3] Processing scan (results from tick 2 still pending)")
    add_scan_result(ship_id, {"target": "ship_2", "tick": 3})
    
    # Now both tick 2 and tick 3 results should be accumulated
    assert ship_id in action_results
    
    # Client polls
    print("[CLIENT] Polling /updates endpoint again")
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    assert results["move_result"]["tick"] == 2  # From tick 2
    assert results["scan_data"]["tick"] == 3   # From tick 3 (overwrote tick 1)
    assert results["attack_result"] is None     # Cleared from last poll
    print(f"[CLIENT] Got results: move={results['move_result']['destination']}, scan={results['scan_data']['target']}")
    
    # Results should be cleared
    assert ship_id not in action_results
    
    print("\n[PASS] API workflow with early returns works correctly")


def test_api_workflow_missed_polls():
    """Simulate client missing several polls (high latency scenario).
    
    Scenario:
    - Tick 1-5: Ship performs various actions
    - Client doesn't poll
    - Client finally polls and gets latest state
    """
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 2000
    
    print("\n[SCENARIO] Client has high latency, missing several ticks")
    
    # Tick 1
    add_scan_result(ship_id, {"target": "location_A", "tick": 1})
    
    # Tick 2
    add_attack_result(ship_id, {"target": "ship_X", "tick": 2})
    
    # Tick 3
    add_move_result(ship_id, {"destination": "Jupiter", "tick": 3})
    
    # Tick 4
    add_scan_result(ship_id, {"target": "location_B", "tick": 4})  # Overwrites tick 1 scan
    
    # Tick 5
    add_attack_result(ship_id, {"target": "ship_Y", "tick": 5})  # Overwrites tick 2 attack
    
    # All results should be accumulated
    assert ship_id in action_results
    
    # Client finally polls
    print("[CLIENT] Finally polling after 5 ticks")
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    
    # Should have latest scan (tick 4), latest attack (tick 5), and move (tick 3)
    assert results["scan_data"]["tick"] == 4
    assert results["attack_result"]["tick"] == 5
    assert results["move_result"]["tick"] == 3
    
    print(f"[CLIENT] Got accumulated results:")
    print(f"  - Latest scan: {results['scan_data']['target']} (tick {results['scan_data']['tick']})")
    print(f"  - Latest attack: {results['attack_result']['target']} (tick {results['attack_result']['tick']})")
    print(f"  - Move: {results['move_result']['destination']} (tick {results['move_result']['tick']})")
    
    # Results should be cleared
    assert ship_id not in action_results
    
    print("\n[PASS] Missed polls scenario works correctly")


def test_api_workflow_no_actions_this_tick():
    """Simulate ticks where ship performs no actions.
    
    Scenario:
    - Tick 1: Ship scans
    - Tick 2: Ship does nothing
    - Client polls (should still get tick 1 results)
    """
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 3000
    
    print("\n[SCENARIO] Ship performs action, then idles")
    
    # Tick 1
    print("[TICK 1] Ship scans")
    add_scan_result(ship_id, {"target": "station", "tick": 1})
    
    # Tick 2: Ship does nothing (no add_* calls)
    print("[TICK 2] Ship idles (no actions)")
    
    # Results from tick 1 should still be there
    assert ship_id in action_results
    
    # Client polls
    print("[CLIENT] Polling after idle tick")
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    assert results["scan_data"]["tick"] == 1
    
    print(f"[CLIENT] Got results from tick 1: {results['scan_data']['target']}")
    
    # Results should be cleared
    assert ship_id not in action_results
    
    # Client polls again (no results)
    print("[CLIENT] Polling again (no pending results)")
    results = get_and_clear_action_results(ship_id)
    assert results is None
    
    print("\n[PASS] Idle tick scenario works correctly")


if __name__ == "__main__":
    test_api_workflow_early_return()
    test_api_workflow_missed_polls()
    test_api_workflow_no_actions_this_tick()
    print("\n" + "="*60)
    print("[PASS] All API workflow tests passed!")
    print("="*60)
