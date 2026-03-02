# Aidan Orion 2 Mar 2026
# Unit tests for IDGenerator

import unittest
import time
from threading import Thread
from id_generator import IDGenerator, ENTITY_TYPE_SHIP, ENTITY_TYPE_ITEM, ENTITY_TYPE_PLAYER, ENTITY_TYPE_FACTION


class TestIDGenerator(unittest.TestCase):
    """Test suite for the IDGenerator class."""
    
    def test_basic_id_generation(self):
        """Test that IDs are generated and are unique."""
        generator = IDGenerator()
        
        # Generate some IDs
        id1 = generator.next_ship_id()
        id2 = generator.next_ship_id()
        id3 = generator.next_item_id()
        
        # All IDs should be different
        self.assertNotEqual(id1, id2)
        self.assertNotEqual(id1, id3)
        self.assertNotEqual(id2, id3)
        
        # All IDs should be positive integers
        self.assertGreater(id1, 0)
        self.assertGreater(id2, 0)
        self.assertGreater(id3, 0)
    
    def test_different_entity_types(self):
        """Test that different entity types generate different IDs."""
        generator = IDGenerator()
        
        ship_id = generator.next_ship_id()
        item_id = generator.next_item_id()
        player_id = generator.next_player_id()
        faction_id = generator.next_faction_id()
        
        # All should be different
        ids = [ship_id, item_id, player_id, faction_id]
        self.assertEqual(len(ids), len(set(ids)), "All entity type IDs should be unique")
        
        # Extract entity types
        ship_type = generator._extract_entity_type(ship_id)
        item_type = generator._extract_entity_type(item_id)
        player_type = generator._extract_entity_type(player_id)
        faction_type = generator._extract_entity_type(faction_id)
        
        self.assertEqual(ship_type, ENTITY_TYPE_SHIP)
        self.assertEqual(item_type, ENTITY_TYPE_ITEM)
        self.assertEqual(player_type, ENTITY_TYPE_PLAYER)
        self.assertEqual(faction_type, ENTITY_TYPE_FACTION)
    
    def test_sequential_ids_same_type(self):
        """Test that sequential IDs for the same type increment properly."""
        generator = IDGenerator()
        
        # Generate 1000 ship IDs rapidly
        ids = [generator.next_ship_id() for _ in range(1000)]
        
        # All should be unique
        self.assertEqual(len(ids), len(set(ids)), "All IDs should be unique")
        
        # All should be ship type
        for id_val in ids:
            entity_type = generator._extract_entity_type(id_val)
            self.assertEqual(entity_type, ENTITY_TYPE_SHIP)
    
    def test_recovery_from_existing_ids(self):
        """Test that generator correctly recovers from existing IDs."""
        # Create first generator and generate some IDs
        gen1 = IDGenerator()
        existing_ids = [gen1.next_ship_id() for _ in range(10)]
        existing_ids.extend([gen1.next_item_id() for _ in range(10)])
        
        max_existing = max(existing_ids)
        
        # Create second generator with existing IDs
        gen2 = IDGenerator(existing_ids=existing_ids)
        
        # New IDs should be higher than all existing IDs
        new_ship_id = gen2.next_ship_id()
        new_item_id = gen2.next_item_id()
        
        # Extract timestamps to verify they're >= existing
        new_ship_ts = gen2._extract_timestamp(new_ship_id)
        new_item_ts = gen2._extract_timestamp(new_item_id)
        max_existing_ts = max(gen2._extract_timestamp(id_val) for id_val in existing_ids if id_val >= 1_000_000)
        
        self.assertGreaterEqual(new_ship_ts, max_existing_ts)
        self.assertGreaterEqual(new_item_ts, max_existing_ts)
        
        # New IDs should not collide with existing
        self.assertNotIn(new_ship_id, existing_ids)
        self.assertNotIn(new_item_id, existing_ids)
    
    def test_clock_offset_applied(self):
        """Test that clock offset prevents duplicates when clock goes backwards."""
        # Create first generator and generate IDs
        gen1 = IDGenerator()
        existing_ids = [gen1.next_ship_id() for _ in range(5)]
        
        # Simulate clock going backwards by creating new generator with existing IDs
        # The new generator should detect and apply an offset
        gen2 = IDGenerator(existing_ids=existing_ids)
        
        # New generator might have an offset
        # Generate new IDs and ensure no duplicates
        new_ids = [gen2.next_ship_id() for _ in range(5)]
        
        # No overlap between old and new
        combined = set(existing_ids + new_ids)
        self.assertEqual(len(combined), 10, "No duplicate IDs should exist")
    
    def test_concurrent_id_generation(self):
        """Test that ID generation is thread-safe."""
        generator = IDGenerator()
        results = []
        
        def generate_ids(count):
            """Generate IDs in a thread."""
            thread_ids = [generator.next_ship_id() for _ in range(count)]
            results.extend(thread_ids)
        
        # Create 10 threads, each generating 100 IDs
        threads = []
        for _ in range(10):
            thread = Thread(target=generate_ids, args=(100,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Should have 1000 unique IDs
        self.assertEqual(len(results), 1000)
        self.assertEqual(len(set(results)), 1000, "All concurrent IDs should be unique")
    
    def test_high_volume_generation(self):
        """Test generating many IDs rapidly (stress test)."""
        generator = IDGenerator()
        
        # Generate 10,000 IDs as fast as possible
        start_time = time.time()
        ids = [generator.next_ship_id() for _ in range(10_000)]
        elapsed = time.time() - start_time
        
        # All should be unique
        self.assertEqual(len(set(ids)), 10_000)
        
        # Should complete quickly (< 1 second for 10k IDs)
        self.assertLess(elapsed, 1.0, f"Should generate 10k IDs in < 1s (took {elapsed:.3f}s)")
        
        print(f"\n[Performance] Generated 10,000 IDs in {elapsed*1000:.2f}ms ({10_000/elapsed:.0f} IDs/sec)")
    
    def test_extract_methods(self):
        """Test ID component extraction methods."""
        generator = IDGenerator()
        
        ship_id = generator.next_ship_id()
        
        # Extract components
        timestamp = generator._extract_timestamp(ship_id)
        entity_type = generator._extract_entity_type(ship_id)
        sequence = generator._extract_sequence(ship_id)
        
        # Verify types
        self.assertIsInstance(timestamp, int)
        self.assertIsInstance(entity_type, int)
        self.assertIsInstance(sequence, int)
        
        # Verify ranges
        self.assertGreaterEqual(timestamp, 0)
        self.assertEqual(entity_type, ENTITY_TYPE_SHIP)
        self.assertGreaterEqual(sequence, 0)
        self.assertLess(sequence, 4096)  # Max sequence is 4095
    
    def test_ignore_old_test_ids(self):
        """Test that old test IDs (< 1,000,000) are ignored during recovery."""
        # Create generator with mix of old test IDs and new IDs
        gen1 = IDGenerator()
        new_ids = [gen1.next_ship_id() for _ in range(5)]
        
        # Mix with old test IDs
        old_test_ids = [1, 2, 100, 200, 500]
        mixed_ids = old_test_ids + new_ids
        
        # Create new generator with mixed IDs
        gen2 = IDGenerator(existing_ids=mixed_ids)
        
        # Should only consider the new IDs for recovery
        next_id = gen2.next_ship_id()
        
        # Next ID should be based on new_ids, not old test IDs
        self.assertNotIn(next_id, mixed_ids)
        self.assertGreater(next_id, max(new_ids))


if __name__ == '__main__':
    unittest.main(verbosity=2)
