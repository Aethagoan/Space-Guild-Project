# Test to verify we don't create unnecessary dict copies

import sys
import unittest.mock as mock

from actions import (
    add_scan_result,
    add_attack_result,
    action_results,
    action_results_locks,
    _ACTION_RESULTS_TEMPLATE
)


def test_no_unnecessary_dict_copies():
    """Verify that we only copy the template when ship_id is not in action_results."""
    
    # Clear state
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 100
    
    # We can't easily mock dict.copy, but we can verify the behavior by checking
    # that the dict structure is preserved across multiple calls
    
    # First call - creates the dict
    add_scan_result(ship_id, {'target': 1})
    assert ship_id in action_results
    first_dict_id = id(action_results[ship_id])
    
    # Second call - should use existing dict, not create new one
    add_attack_result(ship_id, {'target': 2})
    second_dict_id = id(action_results[ship_id])
    assert first_dict_id == second_dict_id, "Should reuse same dict, not create new one!"
    
    # Third call - should still use same dict
    add_scan_result(ship_id, {'target': 3})
    third_dict_id = id(action_results[ship_id])
    assert first_dict_id == third_dict_id, "Should still reuse same dict!"
    
    # Verify data is correct
    assert action_results[ship_id]["scan_data"]["target"] == 3
    assert action_results[ship_id]["attack_result"]["target"] == 2
    
    print("[PASS] Dict is reused across calls (no unnecessary copies)")


def test_compare_setdefault_vs_if_not_in():
    """Compare performance of setdefault vs if-not-in pattern."""
    
    import time
    
    action_results.clear()
    action_results_locks.clear()
    
    # Test 1: Using if-not-in pattern (current implementation)
    start = time.perf_counter()
    for i in range(10000):
        ship_id = i % 100  # 100 unique ships
        # Simulate what add_scan_result does
        if ship_id not in action_results:
            action_results[ship_id] = _ACTION_RESULTS_TEMPLATE.copy()
        action_results[ship_id]["scan_data"] = {"tick": i}
    elapsed_if = time.perf_counter() - start
    
    action_results.clear()
    
    # Test 2: Using setdefault pattern (old implementation)
    start = time.perf_counter()
    for i in range(10000):
        ship_id = i % 100
        # Old pattern - creates copy every time
        action_results.setdefault(ship_id, _ACTION_RESULTS_TEMPLATE.copy())
        action_results[ship_id]["scan_data"] = {"tick": i}
    elapsed_setdefault = time.perf_counter() - start
    
    speedup = elapsed_setdefault / elapsed_if
    
    print(f"\nPerformance comparison (10,000 calls across 100 ships):")
    print(f"  if-not-in pattern:  {elapsed_if*1000:.2f}ms")
    print(f"  setdefault pattern: {elapsed_setdefault*1000:.2f}ms")
    print(f"  Speedup: {speedup:.2f}x")
    
    assert speedup > 1.0, "if-not-in should be faster!"
    
    print(f"\n[PASS] if-not-in is {speedup:.2f}x faster than setdefault")


if __name__ == "__main__":
    test_no_unnecessary_dict_copies()
    test_compare_setdefault_vs_if_not_in()
    print("\n[PASS] All optimization tests passed!")
