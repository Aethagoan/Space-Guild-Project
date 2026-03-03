"""
Test the /updates endpoint with concurrent requests and condition variables.
Tests the semaphore-based blocking approach for scalability.

Aidan Orion 2 Mar 2026
"""

import threading
import time
import sys
from data import DataHandler
from threading import Event
import actions

# Mock tick completion event (simulates program.py)
tick_completion_event = Event()

# Set up minimal globals for api.py to import
sys.modules['program'] = type(sys)('program')
sys.modules['program'].data_handler = DataHandler(data_dir="test_game_data", create_dir=False)
sys.modules['program'].tick_completion_event = tick_completion_event


def test_concurrent_blocking_requests(num_clients=100):
    """Test multiple clients blocking on /updates endpoint simultaneously.
    
    This simulates the real-world scenario where many players are waiting
    for the next tick to complete.
    """
    print(f"\n[TEST] Simulating {num_clients} concurrent /updates requests...")
    
    # Import api after setting up mocks
    import api
    from flask import Flask
    
    # Set up test data
    dh = sys.modules['program'].data_handler
    dh.Locations = {}
    dh.Ships = {}
    dh.Players = {}
    dh.Items = {}
    
    # Create test location
    dh.Locations['TestLoc'] = {
        'name': 'TestLoc',
        'description': 'Test',
        'links': [],
        'ship_ids': [],
        'visible_ship_ids': [],
        'items': []
    }
    
    # Create test players and ships
    for i in range(num_clients):
        player_id = i + 1
        ship_id = i + 1
        
        dh.Players[player_id] = {
            'id': player_id,
            'name': f'Player{player_id}',
            'ship_id': ship_id
        }
        
        dh.Ships[ship_id] = {
            'hp': 100.0,
            'tier': 1,
            'location': 'TestLoc',
            'shield_pool': 0.0,
            'engine_id': None,
            'weapon_id': None,
            'shield_id': None,
            'cargo_id': None,
            'sensor': None,
            'stealth_cloak_id': None,
            'items': []
        }
    
    # Set up Flask test client
    app = api.app
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Track request results
    results = []
    request_times = []
    errors = []
    
    def make_request(player_id):
        """Make a blocking /updates request"""
        start_time = time.time()
        try:
            response = client.get(f'/updates?player_id={player_id}')
            elapsed = time.time() - start_time
            
            request_times.append(elapsed)
            
            if response.status_code == 200:
                results.append((player_id, 'success', elapsed))
            else:
                results.append((player_id, f'error_{response.status_code}', elapsed))
        except Exception as e:
            elapsed = time.time() - start_time
            errors.append((player_id, str(e)))
            results.append((player_id, 'exception', elapsed))
    
    # Start all client threads
    threads = []
    print(f"  [*] Starting {num_clients} request threads...")
    start = time.time()
    
    for i in range(num_clients):
        player_id = i + 1
        t = threading.Thread(target=make_request, args=(player_id,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Give threads time to all register and start waiting
    time.sleep(0.5)
    print(f"  [*] All threads waiting on condition variables...")
    print(f"  [*] Active waiting clients: {len(api.pending_updates)}")
    
    # Simulate tick completion after 2 seconds
    time.sleep(2.0)
    print(f"  [*] Simulating tick completion - notifying all clients...")
    notify_start = time.time()
    
    tick_completion_event.set()
    api.notify_all_waiting_clients()
    
    notify_duration = time.time() - notify_start
    print(f"  [*] Notification took: {notify_duration*1000:.2f}ms")
    
    # Wait for all threads to complete (with timeout)
    print(f"  [*] Waiting for all threads to complete...")
    for t in threads:
        t.join(timeout=5.0)
    
    total_duration = time.time() - start
    
    # Analyze results
    successful = len([r for r in results if r[1] == 'success'])
    failed = len(results) - successful
    
    print(f"\n[RESULTS]")
    print(f"  Total clients: {num_clients}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Errors: {len(errors)}")
    print(f"  Total duration: {total_duration:.3f}s")
    
    if request_times:
        avg_time = sum(request_times) / len(request_times)
        min_time = min(request_times)
        max_time = max(request_times)
        print(f"  Request times - Avg: {avg_time:.3f}s, Min: {min_time:.3f}s, Max: {max_time:.3f}s")
    
    if errors:
        print(f"\n[ERRORS]")
        for player_id, error in errors[:5]:  # Show first 5 errors
            print(f"  Player {player_id}: {error}")
    
    # Validation
    assert successful > 0, "No requests succeeded!"
    assert successful >= num_clients * 0.9, f"Too many failures: {failed}/{num_clients}"
    
    # All requests should complete around the same time (~2 seconds wait)
    # With many clients, notification time adds overhead
    if request_times:
        assert min(request_times) >= 2.0, "Request completed too early (before tick)"
        # Allow up to 10s for large client counts (notification overhead)
        max_allowed = 10.0 if num_clients > 5000 else 5.0
        assert max(request_times) < max_allowed, f"Request took too long: {max(request_times):.2f}s"
    
    print(f"\n[PASS] Concurrent blocking test passed!")
    
    # Cleanup
    tick_completion_event.clear()
    api.pending_updates.clear()


def test_condition_variable_efficiency():
    """Test that condition variables don't busy-wait (CPU should be idle)"""
    print(f"\n[TEST] Verifying condition variables sleep efficiently...")
    
    import api
    from threading import Condition
    import psutil
    import os
    
    # Get current process
    process = psutil.Process(os.getpid())
    
    # Create condition and start waiting thread
    condition = Condition()
    waiting = [False]
    
    def wait_on_condition():
        waiting[0] = True
        with condition:
            condition.wait(timeout=5.0)
        waiting[0] = False
    
    # Measure CPU usage while waiting
    cpu_before = process.cpu_percent(interval=0.1)
    
    t = threading.Thread(target=wait_on_condition)
    t.daemon = True
    t.start()
    
    time.sleep(0.2)  # Let thread start waiting
    
    # CPU should be near 0% while waiting
    cpu_during = process.cpu_percent(interval=1.0)
    
    # Wake up thread
    with condition:
        condition.notify()
    t.join()
    
    print(f"  CPU usage during wait: {cpu_during:.2f}%")
    print(f"  Thread was waiting: {waiting[0] == False}")
    
    # CPU should be low (< 5%) during wait
    assert cpu_during < 5.0, f"CPU too high during wait: {cpu_during}%"
    
    print(f"[PASS] Condition variables are efficient (not busy-waiting)")


def test_notification_scaling():
    """Test how notification time scales with number of waiting clients"""
    print(f"\n[TEST] Testing notification scaling...")
    
    import api
    from threading import Condition
    
    client_counts = [10, 50, 100, 500, 1000]
    
    print(f"  {'Clients':<10} {'Notify Time':<15} {'Time per Client'}")
    print(f"  {'-'*10} {'-'*15} {'-'*15}")
    
    for num_clients in client_counts:
        # Create conditions
        conditions = [Condition() for _ in range(num_clients)]
        
        # Start waiting threads
        def wait_on_condition(cond):
            with cond:
                cond.wait(timeout=10.0)
        
        threads = []
        for cond in conditions:
            t = threading.Thread(target=wait_on_condition, args=(cond,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(0.1)  # Let threads start waiting
        
        # Measure notification time
        start = time.time()
        for cond in conditions:
            with cond:
                cond.notify()
        notify_time = time.time() - start
        
        # Wait for threads
        for t in threads:
            t.join(timeout=1.0)
        
        time_per_client = (notify_time / num_clients) * 1000000  # microseconds
        
        print(f"  {num_clients:<10} {notify_time*1000:>10.2f}ms     {time_per_client:>10.2f}µs")
    
    print(f"\n[PASS] Notification scaling test complete")


if __name__ == '__main__':
    # Run tests
    try:
        test_concurrent_blocking_requests(num_clients=100)
        
        # Try to test efficiency (requires psutil)
        try:
            import psutil
            test_condition_variable_efficiency()
        except ImportError:
            print("\n[SKIP] psutil not installed - skipping CPU efficiency test")
        
        test_notification_scaling()
        
        print("\n" + "="*70)
        print("[SUCCESS] All concurrency tests passed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
