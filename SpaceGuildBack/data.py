# Aidan Orion 23 Feb 2026

# This is how all of the data for the game is handled.

# Why json and not sql? The tradeoff here is the relational side of it. In this project, there is no use for a relational database except in one and only one place. The rest of the data is unique lines with single id lookups,

# meaning hammering it into a relational database would be somewhat of an increase of CPU usage just based on table logging and other things. I decided to shred the extra weight and get a little bit of a technical challenge.


# standard library imports :)

from collections import defaultdict
from threading import Lock
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple
import json
import os

# -
from location import Location
from player import Player
from ship import Ship
from item import Item
from faction import Faction


# Ship log message types
class MessageType:
    """Predefined message types for ship logs with associated colors."""
    COMBAT = "combat"  # Red - combat-related messages
    ACTION = "action"  # Blue - player/ship actions
    SHIP_MESSAGE = "ship_message"  # Faction color - communication from another ship
    COMPUTER = "computer"  # Green - ship computer messages
    ENVIRONMENT = "environment"  # Yellow - environmental messages
    
    @classmethod
    def all_types(cls) -> List[str]:
        """Get all valid message types."""
        return [cls.COMBAT, cls.ACTION, cls.SHIP_MESSAGE, cls.COMPUTER, cls.ENVIRONMENT]


class DataHandler:
    """Thread-safe data handler for all game entities using JSON storage.
    
    """
    
    def __init__(self, data_dir: str = "game_data", create_dir: bool = True):
        """Initialize the data handler with empty collections and a lock cache.
        
        Args:
            data_dir: Directory where JSON files will be stored
            create_dir: If True, create the data directory. Set to False for tests.
        """
        # A dictionary of locks, cleared each tick. It's similar to a cache.
        self._locks = defaultdict(Lock)
        
        # Data directories for JSON persistence
        self.data_dir = data_dir
        if create_dir:
            os.makedirs(data_dir, exist_ok=True)
        
        # Entity collections
        # Locations use string names as keys
        self.Locations: Dict[str, dict] = {}
        
        # Ships, Items, Players, Factions use integer IDs as keys
        self.Ships: Dict[int, dict] = {}
        self.Items: Dict[int, dict] = {}
        self.Players: Dict[int, dict] = {}
        self.Factions: Dict[int, dict] = {}
        
        # Vendors use location names as keys, each location has a dict of vendor_id -> vendor data
        self.Vendors: Dict[str, Dict[str, dict]] = {}
        
        # Static template data (loaded from setup files, not frequently modified)
        # These are templates/definitions that the game uses to spawn/create actual instances
        self.ResourceItems: Dict[str, dict] = {}  # Resource item templates (e.g., "iron", "platinum")
        self.SpawnableComponents: Dict[str, dict] = {}  # Component spawn templates (e.g., engines, weapons)
        self.SpawnableShips: Dict[str, dict] = {}  # Ship spawn templates (e.g., "orion_enforcers")
        self.NPCFactions: Dict[str, dict] = {}  # NPC faction definitions (e.g., "ORION", "PIRATE")
        
        # Ship logs (ephemeral, not persisted) - lazily initialized
        self.ShipLogs: Dict[int, dict] = {}
        self.MAX_LOG_ENTRIES = 50
    
    def clear_locks(self):
        """Clear the lock cache. Should be called each game tick.
    
        """
        self._locks = defaultdict(Lock)
    
    @contextmanager
    def _acquire_locks(self, *keys):
        """Context manager to acquire multiple locks in sorted order to prevent deadlocks.
        
        Args:
            *keys: Entity keys to lock (will be sorted before acquisition)
        """
        # Sort keys to ensure consistent lock ordering and prevent deadlocks
        # Using (type, str) tuple ensures different types don't conflict
        sorted_keys = sorted(keys, key=lambda k: (type(k).__name__, str(k)))
        locks = [self._locks[key] for key in sorted_keys]
        
        # Acquire all locks in sorted order
        for lock in locks:
            lock.acquire()
        
        try:
            yield
        finally:
            # Release all locks in reverse order (minor optimization: 
            # last-acquired lock released first, potentially unblocking waiters faster)
            for lock in reversed(locks):
                lock.release()
    
    # ============================================================================
    # LOCATION METHODS
    # ============================================================================
    
    def add_location(
        self,
        name: str,
        location_type: str = 'space',
        controlled_by: str = 'ORION',
        description: str = '',
        tags: Optional[List[str]] = None,
        spawnable_ids: Optional[List[str]] = None,
        resource_node_ids: Optional[List[str]] = None,
    ) -> dict:
        """Add a new location to the game.
        
        Args:
            name: Unique name for the location
            location_type: 'space', 'station', 'ground_station', 'resource_node'
            controlled_by: Faction controlling this location (default 'ORION')
            description: Descriptive text about the location
            tags: Safety/danger tags ['Safe', 'Enforced', 'Patrolled', 'Dangerous']
            spawnable_ids: List of IDs for NPCs/ships that can spawn here
            resource_node_ids: List of IDs for resources that can be gathered here
            
        Returns:
            The newly created location dict
            
        Raises:
            KeyError: If location already exists
        """
        if name in self.Locations:
            raise KeyError(f"Location '{name}' already exists")
        
        with self._acquire_locks(f"location:{name}"):
            location = Location(
                name=name,
                location_type=location_type,
                controlled_by=controlled_by,
                description=description,
                tags=tags,
                spawnable_ids=spawnable_ids,
                resource_node_ids=resource_node_ids,
            )
            self.Locations[name] = location
            return location
    
    def get_location(self, name: str) -> dict:
        """Get a location by name (read-only, no lock).
        
        Args:
            name: Location name
            
        Returns:
            The location dict
            
        Raises:
            KeyError: If location doesn't exist
        """
        return self.Locations[name]

    def single_link_locations(self,name1:str,name2:str):
        """Create a one directional link from name1 location to name2 location

        Args:
            name1: First location name
            name2: Second location name
            
        Raises:
            KeyError: If either location doesn't exist
        """
        # Verify both locations exist first
        _ = self.Locations[name1]
        _ = self.Locations[name2]

        # Acquire locks in sorted order to prevent deadlock
        with self._acquire_locks(f"location:{name1}:links"):
            self.Locations[name1]['links'].append(name2)
    
    def double_link_locations(self, name1: str, name2: str):
        """Create a bidirectional link between two locations (thread-safe).
        
        Args:
            name1: First location name
            name2: Second location name
            
        Raises:
            KeyError: If either location doesn't exist
        """
        # Verify both locations exist first
        _ = self.Locations[name1]
        _ = self.Locations[name2]
        
        # Acquire locks in sorted order to prevent deadlock
        with self._acquire_locks(f"location:{name1}:links", f"location:{name2}:links"):
            self.Locations[name1]['links'].append(name2)
            self.Locations[name2]['links'].append(name1)
    
    def add_ship_to_location(self, location_name: str, ship_id: int):
        """Add a ship to a location's ship list (thread-safe).
        
        This syncs both the ship's location field and the location's ship_ids list.
        
        Args:
            location_name: Location to add ship to
            ship_id: ID of ship to add
            
        Raises:
            KeyError: If location or ship doesn't exist
        """
        # Verify both exist
        _ = self.Locations[location_name]
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"location:{location_name}:ships", f"ship:{ship_id}:location"):
            if ship_id not in self.Locations[location_name]['ship_ids']:
                self.Locations[location_name]['ship_ids'].append(ship_id)
            
            # Update ship's location field
            self.Ships[ship_id]['location'] = location_name
    
    def remove_ship_from_location(self, location_name: str, ship_id: int):
        """Remove a ship from a location's ship list (thread-safe).
        
        This syncs both the ship's location field and the location's ship_ids list.
        
        Args:
            location_name: Location to remove ship from
            ship_id: ID of ship to remove
            
        Raises:
            KeyError: If location doesn't exist
            ValueError: If ship is not at that location
        """
        _ = self.Locations[location_name]
        
        with self._acquire_locks(f"location:{location_name}:ships", f"ship:{ship_id}:location"):
            if ship_id in self.Locations[location_name]['ship_ids']:
                self.Locations[location_name]['ship_ids'].remove(ship_id)
                # Clear ship's location field
                self.Ships[ship_id]['location'] = None
            else:
                raise ValueError(f"Ship {ship_id} not found at location '{location_name}'")
    
    def move_ship_between_locations(self, ship_id: int, from_location: str, to_location: str):
        """Move a ship from one location to another (thread-safe with multiple locks).
        
        This syncs both the ship's location field and both locations' ship_ids lists.

        Args:
            ship_id: ID of ship to move
            from_location: Current location name
            to_location: Destination location name
            
        Raises:
            KeyError: If locations or ship don't exist
            ValueError: If ship is not at from_location
        """
        # Verify all entities exist (fail fast before acquiring locks)
        ship = self.Ships[ship_id]
        _ = self.Locations[from_location]
        _ = self.Locations[to_location]
        
        # Acquire locks in sorted order (prevents deadlock if external systems also lock these)
        # - location:{from}:ships - Protects source location's ship list
        # - location:{to}:ships - Protects destination location's ship list  
        # - ship:{id}:location - Protects ship's location field
        with self._acquire_locks(f"location:{from_location}:ships", f"location:{to_location}:ships", f"ship:{ship_id}:location"):
            # Double-check ship is at from_location (both sources of truth)
            # This catches race conditions where ship was moved by another system
            if ship['location'] != from_location:
                raise ValueError(f"Ship {ship_id} location mismatch: ship says '{ship['location']}', expected '{from_location}'")
            
            if ship_id not in self.Locations[from_location]['ship_ids']:
                raise ValueError(f"Ship {ship_id} not in location '{from_location}' ship_ids list")
            
            # Update both sources of truth atomically
            # CRITICAL: These three operations must be atomic to maintain consistency
            self.Locations[from_location]['ship_ids'].remove(ship_id)
            self.Locations[to_location]['ship_ids'].append(ship_id)
            self.Ships[ship_id]['location'] = to_location
    
    def add_item_to_location(self, location_name: str, item_id: int):
        """Add an item to a location's item list (thread-safe).
        
        Args:
            location_name: Location to add item to
            item_id: ID of item to add
            
        Raises:
            KeyError: If location or item doesn't exist
        """
        _ = self.Locations[location_name]
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"location:{location_name}:items"):
            self.Locations[location_name]['items'].append(item_id)
    
    def remove_item_from_location(self, location_name: str, item_id: int):
        """Remove an item from a location's item list (thread-safe).
        
        Args:
            location_name: Location to remove item from
            item_id: ID of item to remove
            
        Raises:
            KeyError: If location doesn't exist
            ValueError: If item is not at that location
        """
        _ = self.Locations[location_name]
        
        with self._acquire_locks(f"location:{location_name}:items"):
            if item_id in self.Locations[location_name]['items']:
                self.Locations[location_name]['items'].remove(item_id)
            else:
                raise ValueError(f"Item {item_id} not found at location '{location_name}'")

    # ============================================================================
    # SHIP METHODS
    # ============================================================================
    
    def add_ship(self, ship_id: int, location_name: str, ship_data: Optional[dict] = None) -> dict:
        """Add a new ship to the game at a specific location.
        
        This syncs both the ship's location field and the location's ship_ids list.
        
        Args:
            ship_id: Unique ID for the ship
            location_name: Starting location for the ship
            ship_data: Optional ship dict (will create default if None)
            
        Returns:
            The newly created ship dict
            
        Raises:
            KeyError: If ship already exists or location doesn't exist
        """
        if ship_id in self.Ships:
            raise KeyError(f"Ship {ship_id} already exists")
        
        # Verify location exists
        _ = self.Locations[location_name]
        
        # Acquire locks for both ship's location and location's ship list
        with self._acquire_locks(f"location:{location_name}:ships", f"ship:{ship_id}:location"):
            ship = ship_data if ship_data is not None else Ship(location=location_name)
            ship['location'] = location_name  # Ensure location is set
            self.Ships[ship_id] = ship
            
            # Add ship to location's ship_ids list
            if ship_id not in self.Locations[location_name]['ship_ids']:
                self.Locations[location_name]['ship_ids'].append(ship_id)
            
            return ship
    
    def get_ship(self, ship_id: int) -> dict:
        """Get a ship by ID (read-only, no lock).
        
        Args:
            ship_id: Ship ID
            
        Returns:
            The ship dict
            
        Raises:
            KeyError: If ship doesn't exist
        """
        return self.Ships[ship_id]
    
    def remove_ship(self, ship_id: int):
        """Remove a ship from the game (thread-safe).
        
        This removes the ship from:
        - The Ships collection
        - Its current location's ship_ids list
        - Any player references (sets player's ship_id to None)
        
        Args:
            ship_id: Ship ID to remove
            
        Raises:
            KeyError: If ship doesn't exist
        """
        ship = self.Ships[ship_id]
        location_name = ship.get('location')
        
        # Acquire locks for ship, location, and any potential player updates
        locks_to_acquire = [f"ship:{ship_id}"]
        if location_name:
            locks_to_acquire.append(f"location:{location_name}:ships")
        
        with self._acquire_locks(*locks_to_acquire):
            # Remove from location's ship list
            if location_name and location_name in self.Locations:
                if ship_id in self.Locations[location_name]['ship_ids']:
                    self.Locations[location_name]['ship_ids'].remove(ship_id)
            
            # Remove from Players (set any player's ship_id to None if they own this ship)
            for player_id, player in self.Players.items():
                if player.get('ship_id') == ship_id:
                    with self._acquire_locks(f"player:{player_id}"):
                        self.Players[player_id]['ship_id'] = None
            
            # Remove from Ships collection
            del self.Ships[ship_id]
    
    def get_ship_location(self, ship_id: int) -> str:
        """Get a ship's current location (O(1) lookup).
        
        Args:
            ship_id: Ship ID
            
        Returns:
            Location name
            
        Raises:
            KeyError: If ship doesn't exist
        """
        return self.Ships[ship_id]['location']
    
    def update_ship_hp(self, ship_id: int, delta: int):
        """Modify a ship's HP (thread-safe).
        
        Args:
            ship_id: Ship ID
            delta: Amount to change HP by (can be negative)
            
        Raises:
            KeyError: If ship doesn't exist
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:hp"):
            self.Ships[ship_id]['hp'] = max(0, self.Ships[ship_id]['hp'] + delta)
    
    def set_ship_hp(self, ship_id: int, hp: int):
        """Set a ship's HP directly (thread-safe).
        
        ⚠️ WARNING: FOR TESTING ONLY! ⚠️
        This method bypasses normal game mechanics and should ONLY be used in tests.
        In production code, use damage_ship_hp() or heal_ship_hp() instead.
        
        Args:
            ship_id: Ship ID
            hp: New HP value
            
        Raises:
            KeyError: If ship doesn't exist
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:hp"):
            self.Ships[ship_id]['hp'] = max(0, hp)
    
    def set_ship_shield_pool(self, ship_id: int, shield_pool: float):
        """Set a ship's shield pool directly (thread-safe).
        
        ⚠️ WARNING: FOR TESTING ONLY! ⚠️
        This method bypasses normal game mechanics and should ONLY be used in tests.
        In production code, use damage_shield_pool() or heal_shield_pool() instead.
        
        Args:
            ship_id: Ship ID
            shield_pool: New shield pool value
            
        Raises:
            KeyError: If ship doesn't exist
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:shield"):
            self.Ships[ship_id]['shield_pool'] = max(0.0, shield_pool)
    
    def set_ship_component(self, ship_id: int, component_type: str, item_id: int):
        """Set a ship's component (engine, weapon, shield, etc.) directly (thread-safe).
        
        Args:
            ship_id: Ship ID
            component_type: One of 'engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id'
            item_id: ID of the new component item
            
        Raises:
            KeyError: If ship or item doesn't exist
            ValueError: If component_type is invalid
        """
        valid_components = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id']
        if component_type not in valid_components:
            raise ValueError(f"Invalid component type '{component_type}'. Must be one of {valid_components}")
        
        _ = self.Ships[ship_id]
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"ship:{ship_id}:component:{component_type}"):
            self.Ships[ship_id][component_type] = item_id
    
    def set_ship_to_max_hp(self, ship_id: int):
        """Set a ship's HP to its maximum based on tier (thread-safe).
        
        This is used for full repairs at stations. 
        Formula: 100 * ((1 + tier) ^ 2)
        
        Args:
            ship_id: Ship ID to heal to max HP
            
        Raises:
            KeyError: If ship doesn't exist
        """
        ship = self.Ships[ship_id]
        tier = ship['tier']
        max_hp = 100.0 * ((1 + tier) ** 2)
        
        with self._acquire_locks(f"ship:{ship_id}:hp"):
            self.Ships[ship_id]['hp'] = max_hp
    
    def set_shield_to_max(self, ship_id: int):
        """Set a ship's shield pool to its maximum capacity (thread-safe).
        
        This is used for refilling shields at stations.
        The max capacity is determined by the equipped shield component.
        Formula: 50 * ((1 + shield_tier) ^ 1.5) * shield_multiplier
        
        Args:
            ship_id: Ship ID to refill shields
            
        Raises:
            KeyError: If ship doesn't exist
        """
        ship = self.Ships[ship_id]
        
        # Get shield component
        shield_id = ship.get('shield_id')
        if shield_id is None or shield_id not in self.Items:
            # No shield equipped, set pool to 0
            with self._acquire_locks(f"ship:{ship_id}:shield"):
                self.Ships[ship_id]['shield_pool'] = 0.0
            return
        
        shield = self.Items[shield_id]
        tier = shield['tier']
        multiplier = shield['multiplier']
        max_shield = 50.0 * ((1 + tier) ** 1.5) * multiplier
        
        with self._acquire_locks(f"ship:{ship_id}:shield"):
            self.Ships[ship_id]['shield_pool'] = max_shield
    
    def add_item_to_ship_cargo(self, ship_id: int, item_id: int):
        """Add an item to a ship's cargo (thread-safe).
        
        Args:
            ship_id: Ship ID
            item_id: Item ID to add to cargo
            
        Raises:
            KeyError: If ship or item doesn't exist
        """
        _ = self.Ships[ship_id]
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"ship:{ship_id}:cargo"):
            self.Ships[ship_id]['items'].append(item_id)
    
    def remove_item_from_ship_cargo(self, ship_id: int, item_id: int):
        """Remove an item from a ship's cargo (thread-safe).
        
        Args:
            ship_id: Ship ID
            item_id: Item ID to remove from cargo
            
        Raises:
            KeyError: If ship doesn't exist
            ValueError: If item is not in cargo
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:cargo"):
            if item_id in self.Ships[ship_id]['items']:
                self.Ships[ship_id]['items'].remove(item_id)
            else:
                raise ValueError(f"Item {item_id} not in ship {ship_id}'s cargo")
    
    # ============================================================================
    # ITEM METHODS
    # ============================================================================
    
    def add_item(self, item_id: int, item_data: dict) -> dict:
        """Add a new item to the game.
        
        Args:
            item_id: Unique ID for the item
            item_data: Item dict (must be provided, use item.py creators)
            
        Returns:
            The newly created item dict
            
        Raises:
            KeyError: If item already exists
        """
        if item_id in self.Items:
            raise KeyError(f"Item {item_id} already exists")
        
        with self._acquire_locks(f"item:{item_id}"):
            self.Items[item_id] = item_data
            return item_data
    
    def get_item(self, item_id: int) -> dict:
        """Get an item by ID (read-only, no lock).
        
        Args:
            item_id: Item ID
            
        Returns:
            The item dict
            
        Raises:
            KeyError: If item doesn't exist
        """
        return self.Items[item_id]
    
    def remove_item(self, item_id: int):
        """Remove an item from the game (thread-safe).
        
        This removes the item from:
        - The Items collection
        - Any ship's cargo (items list)
        - Any ship's equipped component slots
        - Any location's items list
        
        Args:
            item_id: Item ID to remove
            
        Raises:
            KeyError: If item doesn't exist
        """
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"item:{item_id}"):
            # Remove from all ship cargo holds
            for ship_id, ship in self.Ships.items():
                if item_id in ship['items']:
                    with self._acquire_locks(f"ship:{ship_id}:cargo"):
                        ship['items'].remove(item_id)
            
            # Remove from all ship component slots
            component_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id']
            for ship_id, ship in self.Ships.items():
                for slot in component_slots:
                    if ship.get(slot) == item_id:
                        with self._acquire_locks(f"ship:{ship_id}:component:{slot}"):
                            self.Ships[ship_id][slot] = None
                            # If removing shield, clear shield pool
                            if slot == 'shield_id':
                                self.Ships[ship_id]['shield_pool'] = 0.0
            
            # Remove from all locations
            for location_name, location in self.Locations.items():
                if item_id in location['items']:
                    with self._acquire_locks(f"location:{location_name}:items"):
                        location['items'].remove(item_id)
            
            # Remove from Items collection
            del self.Items[item_id]
    
    def update_item_multiplier(self, item_id: int, new_multiplier: float):
        """Update an item's multiplier (thread-safe).
        
        Args:
            item_id: Item ID
            new_multiplier: New multiplier value
            
        Raises:
            KeyError: If item doesn't exist
        """
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"item:{item_id}"):
            # Clamp to min/max multiplier bounds
            min_mult = self.Items[item_id]['min_multiplier']
            max_mult = self.Items[item_id]['max_multiplier']
            self.Items[item_id]['multiplier'] = max(min_mult, min(max_mult, new_multiplier))
    
    def set_item_to_max_health(self, item_id: int):
        """Set an item's health to its maximum (thread-safe).
        
        This is used for full repairs at stations. The max health is calculated
        based on the item's type and tier using standard formulas.
        
        Args:
            item_id: Item ID to heal to max
            
        Raises:
            KeyError: If item doesn't exist
            ValueError: If item type is invalid or not a component
        """
        item = self.Items[item_id]
        item_type = item['type']
        tier = item['tier']
        
        # Calculate max health based on type and tier
        health_formulas = {
            'engine': lambda t: 40.0 * (1 + t),
            'weapon': lambda t: 50.0 * (1 + t),
            'shield': lambda t: 25.0 * (1 + t),
            'cargo': lambda t: 100.0 * (1 + t),
            'sensor': lambda t: 25.0 * (1 + t),
            'stealth_cloak': lambda t: 40.0 * (1 + t),
        }
        
        if item_type not in health_formulas:
            raise ValueError(f"Item type '{item_type}' does not have health (must be a component)")
        
        max_health = health_formulas[item_type](tier)
        
        with self._acquire_locks(f"item:{item_id}"):
            self.Items[item_id]['health'] = max_health
    
    def heal_item_health(self, item_id: int, heal_amount: float):
        """Heal an item's health (thread-safe).
        
        Healing is separate from damage for thread safety and clarity.
        Health will be clamped to max_health.
        
        Args:
            item_id: Item ID to heal
            heal_amount: Amount of health to restore (must be positive)
            
        Raises:
            KeyError: If item doesn't exist
            ValueError: If heal_amount is negative
        """
        if heal_amount < 0:
            raise ValueError(f"heal_amount must be positive, got {heal_amount}")
        
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"item:{item_id}"):
            current_health = self.Items[item_id]['health']
            max_health = self.Items[item_id]['max_health']
            new_health = min(max_health, current_health + heal_amount)
            self.Items[item_id]['health'] = new_health
    
    def set_item_health(self, item_id: int, health: float):
        """Set an item's health directly (thread-safe).
        
        ⚠️ WARNING: FOR TESTING ONLY! ⚠️
        This method bypasses normal game mechanics and should ONLY be used in tests.
        In production code, use damage_item() or heal_item_health() instead.
        
        Args:
            item_id: Item ID
            health: New health value
            
        Raises:
            KeyError: If item doesn't exist
        """
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"item:{item_id}"):
            self.Items[item_id]['health'] = max(0.0, health)
    
    def damage_item(self, item_id: int, damage: float) -> Dict[str, Any]:
        """Apply damage to an item's health (thread-safe).
        
        When an item's health reaches 0, it becomes disabled and stops functioning.
        The item stays equipped but cannot be used until repaired.
        
        Args:
            item_id: Item ID to damage
            damage: Amount of damage to apply
            
        Returns:
            Dict with damage results: {
                'health_damage': float,
                'remaining_health': float,
                'disabled': bool
            }
            
        Raises:
            KeyError: If item doesn't exist
        """
        _ = self.Items[item_id]
        
        with self._acquire_locks(f"item:{item_id}"):
            current_health = self.Items[item_id]['health']
            
            # Apply damage
            health_damage = min(damage, current_health)
            new_health = max(0.0, current_health - damage)
            disabled = new_health <= 0
            
            # Update health
            self.Items[item_id]['health'] = new_health
            
            # If disabled (health <= 0), handle special component behaviors
            if disabled:
                # Check if this is a shield or cargo component and handle special cases
                item_type = self.Items[item_id]['type']
                
                # If shield disabled, clear shield pool of the ship that has it equipped
                if item_type == 'shield':
                    for ship_id in self.Ships:
                        if self.Ships[ship_id].get('shield_id') == item_id:
                            self.Ships[ship_id]['shield_pool'] = 0.0
                            break
                
                # If cargo disabled, spill all items to ship's location
                elif item_type == 'cargo':
                    for ship_id in self.Ships:
                        if self.Ships[ship_id].get('cargo_id') == item_id:
                            # Get ship's location
                            location_name = self.Ships[ship_id]['location']
                            if location_name and location_name in self.Locations:
                                # Transfer all items from ship to location
                                items_to_spill = list(self.Ships[ship_id]['items'])  # Copy list
                                for spill_item_id in items_to_spill:
                                    self.Ships[ship_id]['items'].remove(spill_item_id)
                                    self.Locations[location_name]['items'].append(spill_item_id)
                            break
            
            return {
                'health_damage': health_damage,
                'remaining_health': new_health,
                'disabled': disabled
            }
    
    def damage_ship_hp(self, ship_id: int, damage: float) -> Dict[str, Any]:
        """Apply damage to a ship's HP (thread-safe).
        
        Args:
            ship_id: Ship ID to damage
            damage: Amount of damage to apply
            
        Returns:
            Dict with damage results: {
                'hp_damage': float,
                'remaining_hp': float
            }
            
        Raises:
            KeyError: If ship doesn't exist
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:hp"):
            current_hp = self.Ships[ship_id]['hp']
            
            # Apply damage
            hp_damage = min(damage, current_hp)
            new_hp = max(0.0, current_hp - damage)
            
            # Update HP
            self.Ships[ship_id]['hp'] = new_hp
            
            return {
                'hp_damage': hp_damage,
                'remaining_hp': new_hp
            }
    
    def heal_ship_hp(self, ship_id: int, heal_amount: float):
        """Heal a ship's HP (thread-safe).
        
        Healing is separate from damage for thread safety and clarity.
        HP will be clamped to max_hp.
        
        Args:
            ship_id: Ship ID to heal
            heal_amount: Amount of HP to restore (must be positive)
            
        Raises:
            KeyError: If ship doesn't exist
            ValueError: If heal_amount is negative
        """
        if heal_amount < 0:
            raise ValueError(f"heal_amount must be positive, got {heal_amount}")
        
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:hp"):
            current_hp = self.Ships[ship_id]['hp']
            max_hp = self.Ships[ship_id]['max_hp']
            new_hp = min(max_hp, current_hp + heal_amount)
            self.Ships[ship_id]['hp'] = new_hp
    
    def damage_shield_pool(self, ship_id: int, damage: float) -> Dict[str, Any]:
        """Apply damage to a ship's shield pool (thread-safe).
        
        Args:
            ship_id: Ship ID to damage shields
            damage: Amount of damage to apply
            
        Returns:
            Dict with damage results: {
                'shield_damage': float,
                'remaining_shield': float,
                'overflow_damage': float  # Damage that exceeded shield pool
            }
            
        Raises:
            KeyError: If ship doesn't exist
        """
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:shield"):
            current_shield = self.Ships[ship_id]['shield_pool']
            
            # Calculate how much damage the shield can absorb
            shield_damage = min(damage, current_shield)
            overflow_damage = max(0.0, damage - current_shield)
            new_shield = max(0.0, current_shield - damage)
            
            # Update shield pool
            self.Ships[ship_id]['shield_pool'] = new_shield
            
            return {
                'shield_damage': shield_damage,
                'remaining_shield': new_shield,
                'overflow_damage': overflow_damage
            }
    
    def heal_shield_pool(self, ship_id: int, heal_amount: float):
        """Heal a ship's shield pool (thread-safe).
        
        Healing is separate from damage for thread safety and clarity.
        Shield pool will be clamped to the shield's max capacity.
        
        Args:
            ship_id: Ship ID to heal shields
            heal_amount: Amount of shield to restore (must be positive)
            
        Raises:
            KeyError: If ship doesn't exist
            ValueError: If heal_amount is negative
        """
        if heal_amount < 0:
            raise ValueError(f"heal_amount must be positive, got {heal_amount}")
        
        ship = self.Ships[ship_id]
        
        with self._acquire_locks(f"ship:{ship_id}:shield"):
            # Get max shield capacity from the shield component
            shield_id = ship.get('shield_id')
            if shield_id is None or shield_id not in self.Items:
                # No shield equipped, cannot heal shield pool
                return
            
            shield = self.Items[shield_id]
            max_shield_pool = shield['shield_pool']
            
            current_shield = ship['shield_pool']
            new_shield = min(max_shield_pool, current_shield + heal_amount)
            self.Ships[ship_id]['shield_pool'] = new_shield
    
    # ============================================================================
    # PLAYER METHODS
    # ============================================================================
    
    def add_player(self, player_id: int, player_data: dict) -> dict:
        """Add a new player to the game.
        
        Args:
            player_id: Unique ID for the player
            player_data: Player dict (use Player() from Player.py)
            
        Returns:
            The newly created player dict
            
        Raises:
            KeyError: If player already exists
        """
        if player_id in self.Players:
            raise KeyError(f"Player {player_id} already exists")
        
        with self._acquire_locks(f"player:{player_id}"):
            self.Players[player_id] = player_data
            return player_data
    
    def get_player(self, player_id: int) -> dict:
        """Get a player by ID (read-only, no lock).
        
        Args:
            player_id: Player ID
            
        Returns:
            The player dict
            
        Raises:
            KeyError: If player doesn't exist
        """
        return self.Players[player_id]
    
    def update_player_ship(self, player_id: int, ship_id: int):
        """Update a player's ship (thread-safe).
        
        Args:
            player_id: Player ID
            ship_id: New ship ID
            
        Raises:
            KeyError: If player or ship doesn't exist
        """
        _ = self.Players[player_id]
        _ = self.Ships[ship_id]
        
        with self._acquire_locks(f"player:{player_id}"):
            self.Players[player_id]['ship_id'] = ship_id
    
    def update_player_faction(self, player_id: int, faction_id: int):
        """Update a player's faction (thread-safe).
        
        Args:
            player_id: Player ID
            faction_id: New faction ID
            
        Raises:
            KeyError: If player or faction doesn't exist
        """
        _ = self.Players[player_id]
        _ = self.Factions[faction_id]
        
        with self._acquire_locks(f"player:{player_id}"):
            self.Players[player_id]['faction_id'] = faction_id
    
    # ============================================================================
    # FACTION METHODS
    # ============================================================================
    
    def add_faction(self, faction_id: int, faction_data: dict) -> dict:
        """Add a new faction to the game.
        
        Args:
            faction_id: Unique ID for the faction
            faction_data: Faction dict (use Faction() from faction.py)
            
        Returns:
            The newly created faction dict
            
        Raises:
            KeyError: If faction already exists
        """
        if faction_id in self.Factions:
            raise KeyError(f"Faction {faction_id} already exists")
        
        with self._acquire_locks(f"faction:{faction_id}"):
            self.Factions[faction_id] = faction_data
            return faction_data
    
    def get_faction(self, faction_id: int) -> dict:
        """Get a faction by ID (read-only, no lock).
        
        Args:
            faction_id: Faction ID
            
        Returns:
            The faction dict
            
        Raises:
            KeyError: If faction doesn't exist
        """
        return self.Factions[faction_id]
    
    def add_player_to_faction(self, faction_id: int, player_id: int):
        """Add a player to a faction's player list (thread-safe).
        
        Args:
            faction_id: Faction ID
            player_id: Player ID to add
            
        Raises:
            KeyError: If faction or player doesn't exist
        """
        _ = self.Factions[faction_id]
        _ = self.Players[player_id]
        
        with self._acquire_locks(f"faction:{faction_id}"):
            if player_id not in self.Factions[faction_id]['player_ids']:
                self.Factions[faction_id]['player_ids'].append(player_id)
    
    def remove_player_from_faction(self, faction_id: int, player_id: int):
        """Remove a player from a faction's player list (thread-safe).
        
        Args:
            faction_id: Faction ID
            player_id: Player ID to remove
            
        Raises:
            KeyError: If faction doesn't exist
            ValueError: If player is not in that faction
        """
        _ = self.Factions[faction_id]
        
        with self._acquire_locks(f"faction:{faction_id}"):
            if player_id in self.Factions[faction_id]['player_ids']:
                self.Factions[faction_id]['player_ids'].remove(player_id)
            else:
                raise ValueError(f"Player {player_id} not in faction {faction_id}")
    
    # ============================================================================
    # COMPOSITE HELPER METHODS
    # ============================================================================
    
    def move_item_location_to_ship(self, item_id: int, location_name: str, ship_id: int):
        """Move an item from a location to a ship's cargo (thread-safe, atomic).
        
        The ship must be at the specified location for the transfer to succeed.
        
        Args:
            item_id: ID of item to move
            location_name: Location the item is currently at
            ship_id: Ship to move the item to (must be at location_name)
            
        Raises:
            KeyError: If item, location, or ship doesn't exist
            ValueError: If item is not at the specified location, or ship is not at the location
        """
        # Verify all entities exist
        _ = self.Items[item_id]
        _ = self.Locations[location_name]
        ship = self.Ships[ship_id]
        
        # Verify ship is at the location
        if ship['location'] != location_name:
            raise ValueError(f"Ship {ship_id} is at '{ship['location']}', not at '{location_name}'")
        
        # Acquire locks in sorted order (location items before ship cargo to prevent deadlock)
        with self._acquire_locks(f"location:{location_name}:items", f"ship:{ship_id}:cargo"):
            # Verify item is at the location
            if item_id not in self.Locations[location_name]['items']:
                raise ValueError(f"Item {item_id} not found at location '{location_name}'")
            
            # Atomic transfer: remove from location, add to ship cargo
            self.Locations[location_name]['items'].remove(item_id)
            self.Ships[ship_id]['items'].append(item_id)
    
    def move_item_ship_to_location(self, item_id: int, ship_id: int, location_name: str):
        """Move an item from a ship's cargo to a location (thread-safe, atomic).
        
        The ship must be at the specified location for the transfer to succeed.
        Stations (location_type 'station' or 'ground_station') do not allow item drops.
        
        Args:
            item_id: ID of item to move
            ship_id: Ship the item is currently in (must be at location_name)
            location_name: Location to move the item to
            
        Raises:
            KeyError: If item, ship, or location doesn't exist
            ValueError: If item is not in ship's cargo, ship is not at the location, or location is a station
        """
        # Verify all entities exist
        _ = self.Items[item_id]
        ship = self.Ships[ship_id]
        location = self.Locations[location_name]
        
        # Verify ship is at the location
        if ship['location'] != location_name:
            raise ValueError(f"Ship {ship_id} is at '{ship['location']}', not at '{location_name}'")
        
        # Prevent drops at stations
        location_type = location['location_type']
        if location_type in ['station', 'ground_station']:
            raise ValueError(f"Cannot drop items at {location_type} '{location_name}'")
        
        # Acquire locks in sorted order (location items before ship cargo to prevent deadlock)
        with self._acquire_locks(f"location:{location_name}:items", f"ship:{ship_id}:cargo"):
            # Verify item is in ship's cargo
            if item_id not in self.Ships[ship_id]['items']:
                raise ValueError(f"Item {item_id} not in ship {ship_id}'s cargo")
            
            # Atomic transfer: remove from ship cargo, add to location
            self.Ships[ship_id]['items'].remove(item_id)
            self.Locations[location_name]['items'].append(item_id)
    
    def equip_item_to_ship(self, ship_id: int, item_id: int):
        """Equip an item from ship's cargo to the appropriate slot (thread-safe).
        
        The item's 'type' field determines which slot it goes into. If there's already
        an item in that slot, it will be moved to the ship's cargo.
        
        Valid item types and their mappings:
        - 'engine' -> 'engine_id'
        - 'weapon' -> 'weapon_id'
        - 'shield' -> 'shield_id'
        - 'cargo' -> 'cargo_id'
        - 'sensor' -> 'sensor'
        - 'stealth_cloak' -> 'stealth_cloak_id'
        
        Args:
            ship_id: Ship to equip the item on
            item_id: Item to equip (must be in ship's cargo)
            
        Raises:
            KeyError: If ship or item doesn't exist
            ValueError: If item is not in ship's cargo, or item type is invalid/not equippable
        """
        # Verify entities exist
        _ = self.Ships[ship_id]
        item = self.Items[item_id]
        
        # Map item type to ship slot
        type_to_slot = {
            'engine': 'engine_id',
            'weapon': 'weapon_id',
            'shield': 'shield_id',
            'cargo': 'cargo_id',
            'sensor': 'sensor',
            'stealth_cloak': 'stealth_cloak_id',
        }
        
        item_type = item.get('type')
        if item_type not in type_to_slot:
            raise ValueError(f"Item type '{item_type}' cannot be equipped (must be one of {list(type_to_slot.keys())})")
        
        slot_name = type_to_slot[item_type]
        
        # Acquire both cargo and specific component slot locks (sorted to prevent deadlock)
        with self._acquire_locks(f"ship:{ship_id}:cargo", f"ship:{ship_id}:component:{slot_name}"):
            # Verify item is in ship's cargo
            if item_id not in self.Ships[ship_id]['items']:
                raise ValueError(f"Item {item_id} not in ship {ship_id}'s cargo")
            
            # Get the currently equipped item in that slot (if any)
            old_item_id = self.Ships[ship_id].get(slot_name)
            
            # Remove item from cargo
            self.Ships[ship_id]['items'].remove(item_id)
            
            # If there was an old item, move it to cargo
            if old_item_id is not None and isinstance(old_item_id, int) and old_item_id in self.Items:
                self.Ships[ship_id]['items'].append(old_item_id)
            
            # Equip the new item
            self.Ships[ship_id][slot_name] = item_id
    
    def unequip_item_from_ship(self, ship_id: int, slot_name: str):
        """Unequip an item from a ship slot and move it to cargo (thread-safe).
        
        Args:
            ship_id: Ship to unequip from
            slot_name: Slot to unequip ('engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id')
            
        Raises:
            KeyError: If ship doesn't exist
            ValueError: If slot is invalid or already empty
        """
        valid_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id']
        if slot_name not in valid_slots:
            raise ValueError(f"Invalid slot '{slot_name}'. Must be one of {valid_slots}")
        
        _ = self.Ships[ship_id]
        
        # Acquire both cargo and specific component slot locks (sorted to prevent deadlock)
        with self._acquire_locks(f"ship:{ship_id}:cargo", f"ship:{ship_id}:component:{slot_name}"):
            item_id = self.Ships[ship_id].get(slot_name)
            
            if item_id is None or not isinstance(item_id, int):
                raise ValueError(f"Slot '{slot_name}' on ship {ship_id} is already empty")
            
            # Verify item exists
            if item_id not in self.Items:
                raise KeyError(f"Item {item_id} in slot '{slot_name}' doesn't exist in Items")
            
            # If unequipping shield, clear shield pool
            if slot_name == 'shield_id':
                self.Ships[ship_id]['shield_pool'] = 0.0
            
            # Move to cargo
            self.Ships[ship_id]['items'].append(item_id)
            
            # Clear the slot (set to None or int type for type consistency)
            self.Ships[ship_id][slot_name] = None
    
    def switch_ship_component(self, ship_id: int, slot_name: str, item_id: int):
        """Swap a component between a ship slot and the ship's inventory (thread-safe).
        
        This swaps the item in the specified slot with an item from the ship's cargo.
        If the slot is empty, this acts as an equip operation.
        The item being equipped must be in the ship's cargo and of the correct type for the slot.
        
        Special handling for cargo_id:
        - If swapping to a lower-tier cargo, checks that current cargo weight doesn't exceed new capacity
        - This prevents data loss from items being over capacity
        
        Args:
            ship_id: Ship to perform the swap on
            slot_name: Slot to swap ('engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id')
            item_id: Item ID from cargo to swap into the slot
            
        Raises:
            KeyError: If ship or item doesn't exist
            ValueError: If slot is invalid, item is not in cargo, item type doesn't match slot,
                       or cargo capacity would be exceeded
        """
        valid_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id']
        if slot_name not in valid_slots:
            raise ValueError(f"Invalid slot '{slot_name}'. Must be one of {valid_slots}")
        
        # Verify entities exist
        ship = self.Ships[ship_id]
        new_item = self.Items[item_id]
        
        # Map slot to expected item type
        slot_to_type = {
            'engine_id': 'engine',
            'weapon_id': 'weapon',
            'shield_id': 'shield',
            'cargo_id': 'cargo',
            'sensor': 'sensor',
            'stealth_cloak_id': 'stealth_cloak',
        }
        
        expected_type = slot_to_type[slot_name]
        item_type = new_item['type']
        
        if item_type != expected_type:
            raise ValueError(f"Cannot equip item type '{item_type}' into slot '{slot_name}' (expected '{expected_type}')")
        
        # Special check for cargo swaps - validate capacity BEFORE acquiring locks
        if slot_name == 'cargo_id':
            # Calculate new cargo capacity: 100 * (1 + tier) * multiplier
            new_cargo_tier = new_item['tier']
            new_cargo_mult = new_item['multiplier']
            new_capacity = 100.0 * (1 + new_cargo_tier) * new_cargo_mult
            
            # Calculate current total cargo weight (excluding the new cargo item itself)
            total_weight = 0.0
            for cargo_item_id in ship['items']:
                if cargo_item_id == item_id:
                    continue  # Skip the new cargo item we're equipping
                if cargo_item_id in self.Items:
                    total_weight += self.Items[cargo_item_id]['weight']
            
            # Check if current cargo weight exceeds new capacity
            if total_weight > new_capacity:
                raise ValueError(
                    f"Cannot equip cargo (capacity {new_capacity:.1f}): "
                    f"current cargo weight ({total_weight:.1f}) exceeds new capacity"
                )
        
        # Acquire both cargo and specific component slot locks (sorted to prevent deadlock)
        with self._acquire_locks(f"ship:{ship_id}:cargo", f"ship:{ship_id}:component:{slot_name}"):
            # Verify item is in ship's cargo
            if item_id not in self.Ships[ship_id]['items']:
                raise ValueError(f"Item {item_id} not in ship {ship_id}'s cargo")
            
            # Get the currently equipped item in that slot (if any)
            old_item_id = self.Ships[ship_id].get(slot_name)
            
            # Remove new item from cargo
            self.Ships[ship_id]['items'].remove(item_id)
            
            # If there was an old item, move it to cargo
            if old_item_id is not None and isinstance(old_item_id, int) and old_item_id in self.Items:
                self.Ships[ship_id]['items'].append(old_item_id)
            
            # If unequipping shield, clear shield pool (if old item exists)
            if slot_name == 'shield_id' and old_item_id is not None:
                self.Ships[ship_id]['shield_pool'] = 0.0
            
            # Equip the new item
            self.Ships[ship_id][slot_name] = item_id
    
    # ============================================================================
    # JSON PERSISTENCE METHODS
    # ============================================================================
    
    def save_locations(self, filename: Optional[str] = None):
        """Save all locations to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'locations.json')
        """
        filename = filename or os.path.join(self.data_dir, "locations.json")
        with open(filename, 'w') as f:
            json.dump(self.Locations, f, indent=2)
    
    def load_locations(self, filename: Optional[str] = None):
        """Load locations from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'locations.json')
        """
        filename = filename or os.path.join(self.data_dir, "locations.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.Locations = json.load(f)
            
            # Migrate old save files: ensure all locations have visible_ship_ids field
            for location_name, location in self.Locations.items():
                if 'visible_ship_ids' not in location:
                    # Initialize with empty list (will be populated on first tick)
                    location['visible_ship_ids'] = []
    
    def save_ships(self, filename: Optional[str] = None):
        """Save all ships to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'ships.json')
        """
        filename = filename or os.path.join(self.data_dir, "ships.json")
        # Convert int keys to strings for JSON
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.Ships.items()}, f, indent=2)
    
    def load_ships(self, filename: Optional[str] = None):
        """Load ships from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'ships.json')
        """
        filename = filename or os.path.join(self.data_dir, "ships.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                # Convert string keys back to ints
                self.Ships = {int(k): v for k, v in json.load(f).items()}
    
    def save_items(self, filename: Optional[str] = None):
        """Save all items to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'items.json')
        """
        filename = filename or os.path.join(self.data_dir, "items.json")
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.Items.items()}, f, indent=2)
    
    def load_items(self, filename: Optional[str] = None):
        """Load items from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'items.json')
        """
        filename = filename or os.path.join(self.data_dir, "items.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.Items = {int(k): v for k, v in json.load(f).items()}
    
    def save_players(self, filename: Optional[str] = None):
        """Save all players to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'players.json')
        """
        filename = filename or os.path.join(self.data_dir, "players.json")
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.Players.items()}, f, indent=2)
    
    def load_players(self, filename: Optional[str] = None):
        """Load players from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'players.json')
        """
        filename = filename or os.path.join(self.data_dir, "players.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.Players = {int(k): v for k, v in json.load(f).items()}
    
    def save_factions(self, filename: Optional[str] = None):
        """Save all factions to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'factions.json')
        """
        filename = filename or os.path.join(self.data_dir, "factions.json")
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.Factions.items()}, f, indent=2)
    
    def load_factions(self, filename: Optional[str] = None):
        """Load factions from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'factions.json')
        """
        filename = filename or os.path.join(self.data_dir, "factions.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.Factions = {int(k): v for k, v in json.load(f).items()}
    
    def save_vendors(self, filename: Optional[str] = None):
        """Save all vendors to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'vendor_dialogue.json')
        """
        filename = filename or os.path.join(self.data_dir, "vendor_dialogue.json")
        with open(filename, 'w') as f:
            json.dump(self.Vendors, f, indent=2)
    
    def load_vendors(self, filename: Optional[str] = None):
        """Load vendors from a JSON file.
        
        Vendors are stored by location name. Each location can have multiple vendors.
        
        Args:
            filename: Optional custom filename (defaults to 'vendor_dialogue.json')
        """
        filename = filename or os.path.join(self.data_dir, "vendor_dialogue.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.Vendors = json.load(f)
    
    def get_vendors_at_location(self, location_name: str) -> Dict[str, dict]:
        """Get all vendors at a specific location.
        
        Args:
            location_name: Name of the location to get vendors for
            
        Returns:
            Dict mapping vendor_id to vendor data, or empty dict if no vendors at location
        """
        return self.Vendors.get(location_name, {})
    
    # ============================================================================
    # STATIC TEMPLATE DATA METHODS
    # These are templates/definitions loaded once from setup files
    # ============================================================================
    
    def save_resource_items(self, filename: Optional[str] = None):
        """Save resource item templates to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'resource_items.json')
        """
        filename = filename or os.path.join(self.data_dir, "resource_items.json")
        with open(filename, 'w') as f:
            json.dump(self.ResourceItems, f, indent=2)
    
    def load_resource_items(self, filename: Optional[str] = None):
        """Load resource item templates from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'resource_items.json')
        """
        filename = filename or os.path.join(self.data_dir, "resource_items.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.ResourceItems = json.load(f)
    
    def save_spawnable_components(self, filename: Optional[str] = None):
        """Save spawnable component templates to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'spawnable_components.json')
        """
        filename = filename or os.path.join(self.data_dir, "spawnable_components.json")
        with open(filename, 'w') as f:
            json.dump(self.SpawnableComponents, f, indent=2)
    
    def load_spawnable_components(self, filename: Optional[str] = None):
        """Load spawnable component templates from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'spawnable_components.json')
        """
        filename = filename or os.path.join(self.data_dir, "spawnable_components.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.SpawnableComponents = json.load(f)
    
    def save_spawnable_ships(self, filename: Optional[str] = None):
        """Save spawnable ship templates to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'spawnable_ships.json')
        """
        filename = filename or os.path.join(self.data_dir, "spawnable_ships.json")
        with open(filename, 'w') as f:
            json.dump(self.SpawnableShips, f, indent=2)
    
    def load_spawnable_ships(self, filename: Optional[str] = None):
        """Load spawnable ship templates from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'spawnable_ships.json')
        """
        filename = filename or os.path.join(self.data_dir, "spawnable_ships.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.SpawnableShips = json.load(f)
    
    def save_npc_factions(self, filename: Optional[str] = None):
        """Save NPC faction data to a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'npc_factions.json')
        """
        filename = filename or os.path.join(self.data_dir, "npc_factions.json")
        with open(filename, 'w') as f:
            json.dump(self.NPCFactions, f, indent=2)
    
    def load_npc_factions(self, filename: Optional[str] = None):
        """Load NPC faction data from a JSON file.
        
        Args:
            filename: Optional custom filename (defaults to 'npc_factions.json')
        """
        filename = filename or os.path.join(self.data_dir, "npc_factions.json")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.NPCFactions = json.load(f)
    
    # ============================================================================
    # BULK SAVE/LOAD METHODS
    # ============================================================================
    
    def save_all(self):
        """Save all game data to JSON files.
        
        This includes both dynamic game state (locations, ships, items, etc.)
        and static template data (resource items, spawnable ships, NPC factions).
        """
        # Dynamic game state
        self.save_locations()
        self.save_ships()
        self.save_items()
        self.save_players()
        self.save_factions()
        self.save_vendors()
        
        # Static template data
        self.save_resource_items()
        self.save_spawnable_components()
        self.save_spawnable_ships()
        self.save_npc_factions()
    
    def save_dynamic(self):
        """Save only dynamic game state to JSON files.
        
        This saves locations, ships, items, players, and factions.
        Does NOT save static template data (resource items, spawnable ships, vendors, etc.)
        which should only be saved during initial setup.
        
        Use this method during normal game operations to avoid overwriting
        template files that may have been updated in setup_data.
        """
        self.save_locations()
        self.save_ships()
        self.save_items()
        self.save_players()
        self.save_factions()
    
    def load_all(self):
        """Load all game data from JSON files.
        
        This includes both dynamic game state (locations, ships, items, etc.)
        and static template data (resource items, spawnable ships, NPC factions).
        """
        # Dynamic game state
        self.load_locations()
        self.load_ships()
        self.load_items()
        self.load_players()
        self.load_factions()
        self.load_vendors()
        
        # Static template data
        self.load_resource_items()
        self.load_spawnable_components()
        self.load_spawnable_ships()
        self.load_npc_factions()
    
    # ============================================================================
    # SHIP LOG METHODS (Ephemeral - not persisted)
    # ============================================================================
    
    def _init_ship_log(self, ship_id: int):
        """Lazily initialize a ship log structure.
        
        Args:
            ship_id: The ship to initialize logs for
        """
        if ship_id not in self.ShipLogs:
            self.ShipLogs[ship_id] = {
                'entries': [None] * self.MAX_LOG_ENTRIES,
                'count': 0,
                'write_index': self.MAX_LOG_ENTRIES - 1  # Start at end, write backwards
            }
    
    def add_ship_log(self, ship_id: int, message_type: str, content: str, source: Optional[str] = None):
        """Add a log entry to a ship's ephemeral log.
        Writes backwards so newest messages are at lower indices.
        
        Args:
            ship_id: The ship receiving the log entry
            message_type: Type of message (use MessageType constants: 'combat', 'action', 'ship_message', 'computer', 'environment')
            content: The message content
            source: Optional source identifier in format 'type:id' (e.g., 'ship:123', 'location:Sol', 'item:456')
                   If provided, the frontend can request details about this entity
        """
        # Validate message type
        if message_type not in MessageType.all_types():
            raise ValueError(f"Invalid message_type '{message_type}'. Must be one of {MessageType.all_types()}")
        
        with self._acquire_locks(f"shiplog:{ship_id}"):
            self._init_ship_log(ship_id)
            log = self.ShipLogs[ship_id]
            
            # Write to current position
            entry = {
                'type': message_type,
                'content': content
            }
            
            # Add source if provided
            if source is not None:
                entry['source'] = source
            
            log['entries'][log['write_index']] = entry
            
            # Move write pointer backwards (wraps to end when reaching 0)
            log['write_index'] = (log['write_index'] - 1) % self.MAX_LOG_ENTRIES
            
            if log['count'] < self.MAX_LOG_ENTRIES:
                log['count'] += 1
    
    def get_ship_log(self, ship_id: int) -> List[dict]:
        """Get all log entries for a ship in chronological order (oldest first, newest last).
        
        Args:
            ship_id: The ship to retrieve logs for
            
        Returns:
            List of log entries in chronological order (oldest->newest).
            Each entry contains:
                - type: Message type (combat, action, ship_message, computer, environment)
                - content: The log message text
                - source (optional): Source identifier in format "entity_type:entity_id"
                                    (e.g., "ship:123", "location:Sol", "item:456")
        """
        with self._acquire_locks(f"shiplog:{ship_id}"):
            if ship_id not in self.ShipLogs:
                return []
            
            log = self.ShipLogs[ship_id]
            
            if log['count'] < self.MAX_LOG_ENTRIES:
                # Buffer not full yet - messages are in last 'count' slots
                # Return the last count entries
                return log['entries'][-log['count']:]
            else:
                # Buffer wrapped - slice and concatenate
                # write_index points to next write position
                # Oldest message starts at write_index+1
                oldest_idx = (log['write_index'] + 1) % self.MAX_LOG_ENTRIES
                oldest = log['entries'][oldest_idx:]
                newest = log['entries'][:oldest_idx]
                return oldest + newest
