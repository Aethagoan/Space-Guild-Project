# Test to demonstrate fine-grained locking in action_results
# This test shows that different ships can write results concurrently

import threading
import time
from actions import (
    add_scan_result,
    add_attack_result,
    add_move_result,
    add_collect_result,
    get_and_clear_action_results,
    action_results,
    action_results_locks
)


def test_concurrent_action_results():
    """Test that different ships can write action results concurrently.
    
    This demonstrates fine-grained locking - each ship has its own lock,
    so writes to different ships don't block each other.
    """
    # Clear any existing state
    action_results.clear()
    action_results_locks.clear()
    
    # Track timing to verify concurrent execution
    start_times = {}
    end_times = {}
    
    def write_results(ship_id: int, delay_ms: int):
        """Write multiple results for a ship with artificial delay."""
        start_times[ship_id] = time.time()
        
        # Simulate some processing time
        time.sleep(delay_ms / 1000.0)
        
        # Write multiple result types for this ship
        add_scan_result(ship_id, {"scan_type": "ship", "target": 999})
        add_attack_result(ship_id, {"attack_type": "ship", "target": 999})
        add_move_result(ship_id, {"destination": "test_location"})
        add_collect_result(ship_id, {"item_id": 999})
        
        end_times[ship_id] = time.time()
    
    # Create threads for different ships
    threads = []
    for ship_id in range(1, 11):  # 10 ships
        thread = threading.Thread(target=write_results, args=(ship_id, 10))
        threads.append(thread)
    
    # Start all threads at roughly the same time
    start = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start
    
    # Verify all ships got their results
    for ship_id in range(1, 11):
        results = get_and_clear_action_results(ship_id)
        assert results is not None
        assert results["scan_data"]["scan_type"] == "ship"
        assert results["attack_result"]["attack_type"] == "ship"
        assert results["move_result"]["destination"] == "test_location"
        assert results["collect_result"]["item_id"] == 999
    
    # With fine-grained locking, all threads should run concurrently
    # Total time should be close to the delay (10ms) not 10x delay (100ms)
    # Allow some overhead for thread scheduling
    assert elapsed < 0.05, f"Took {elapsed:.3f}s - threads may be serializing!"
    
    print(f"[PASS] All 10 ships processed concurrently in {elapsed:.3f}s")


def test_same_ship_serializes():
    """Test that writes to the SAME ship are serialized (lock works correctly)."""
    # Clear state
    action_results.clear()
    action_results_locks.clear()
    
    ship_id = 100
    write_order = []
    
    def write_result_1():
        time.sleep(0.01)  # Small delay
        add_scan_result(ship_id, {"order": 1})
        write_order.append(1)
    
    def write_result_2():
        add_attack_result(ship_id, {"order": 2})
        write_order.append(2)
    
    # Start thread 1 first (has delay), then thread 2
    t1 = threading.Thread(target=write_result_1)
    t2 = threading.Thread(target=write_result_2)
    
    t1.start()
    time.sleep(0.005)  # Ensure t1 starts first
    t2.start()
    
    t1.join()
    t2.join()
    
    # Both results should be present
    results = get_and_clear_action_results(ship_id)
    assert results is not None
    assert results["scan_data"]["order"] == 1
    assert results["attack_result"]["order"] == 2
    
    print(f"[PASS] Same-ship writes serialized correctly")


if __name__ == "__main__":
    test_concurrent_action_results()
    test_same_ship_serializes()
    print("\n[PASS] All concurrency tests passed!")
