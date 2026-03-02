# Aidan Orion 2 Mar 2026
# ID Generator - Snowflake-style 64-bit unique ID generation

import time
from threading import Lock
from typing import Optional

# Custom epoch: January 1, 2024 00:00:00 UTC
# This extends the usable timestamp range compared to Unix epoch
EPOCH_START = 1704067200000  # milliseconds since Unix epoch (Jan 1, 2024)

# Bit allocation for 64-bit IDs:
# | 42 bits: Timestamp (ms since EPOCH_START) | 10 bits: Entity Type | 12 bits: Sequence |
TIMESTAMP_BITS = 42
ENTITY_TYPE_BITS = 10
SEQUENCE_BITS = 12

# Bit shifts for packing the ID
SEQUENCE_SHIFT = 0
ENTITY_TYPE_SHIFT = SEQUENCE_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + ENTITY_TYPE_BITS

# Maximum values for each field
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1  # 4095
MAX_ENTITY_TYPE = (1 << ENTITY_TYPE_BITS) - 1  # 1023
MAX_TIMESTAMP = (1 << TIMESTAMP_BITS) - 1  # ~139 years

# Entity type constants
ENTITY_TYPE_SHIP = 0
ENTITY_TYPE_ITEM = 1
ENTITY_TYPE_PLAYER = 2
ENTITY_TYPE_FACTION = 3


class IDGenerator:
    """Thread-safe Snowflake-style ID generator.
    
    Generates unique 64-bit IDs with the following structure:
    - 42 bits: Timestamp in milliseconds since custom epoch (Jan 1, 2024)
    - 10 bits: Entity type (ship, item, player, faction)
    - 12 bits: Sequence number (allows 4096 IDs per millisecond per type)
    
    Features:
    - Thread-safe with per-entity-type locks
    - Handles clock regression via offset calculation
    - Can generate 4M+ IDs per second per entity type
    - Recovers state from existing IDs on initialization
    """
    
    def __init__(self, existing_ids: Optional[list[int]] = None):
        """Initialize the ID generator.
        
        Args:
            existing_ids: List of existing IDs to recover state from (optional).
                         Used on game load to prevent duplicate IDs.
        """
        # Per-entity-type state tracking
        self._last_timestamp: dict[int, int] = {}  # entity_type -> last timestamp used
        self._sequence: dict[int, int] = {}  # entity_type -> current sequence number
        self._locks: dict[int, Lock] = {}  # entity_type -> lock
        
        # Clock offset to handle system time going backwards
        self._clock_offset = 0
        
        # Initialize locks for all entity types
        for entity_type in [ENTITY_TYPE_SHIP, ENTITY_TYPE_ITEM, ENTITY_TYPE_PLAYER, ENTITY_TYPE_FACTION]:
            self._locks[entity_type] = Lock()
            self._last_timestamp[entity_type] = -1
            self._sequence[entity_type] = 0
        
        # If existing IDs provided, recover state to prevent duplicates
        if existing_ids:
            self._recover_from_existing_ids(existing_ids)
    
    def _recover_from_existing_ids(self, existing_ids: list[int]):
        """Analyze existing IDs and set state to prevent duplicates.
        
        Args:
            existing_ids: List of all existing IDs in the system
        """
        if not existing_ids:
            return
        
        # Extract timestamps and entity types from all existing IDs
        max_timestamp_overall = 0
        
        for id_val in existing_ids:
            # Only process IDs that look like Snowflake IDs (large enough)
            # Skip old test IDs like 1, 2, 100, 200
            if id_val < 1_000_000:
                continue
            
            timestamp = self._extract_timestamp(id_val)
            entity_type = self._extract_entity_type(id_val)
            sequence = self._extract_sequence(id_val)
            
            # Track the highest timestamp seen for each entity type
            if entity_type in self._last_timestamp:
                if timestamp > self._last_timestamp[entity_type]:
                    self._last_timestamp[entity_type] = timestamp
                    self._sequence[entity_type] = sequence
                elif timestamp == self._last_timestamp[entity_type]:
                    # Same timestamp, track highest sequence
                    self._sequence[entity_type] = max(self._sequence[entity_type], sequence)
            
            # Track overall max timestamp
            max_timestamp_overall = max(max_timestamp_overall, timestamp)
        
        # Calculate clock offset if current time is behind max timestamp
        current_time = self._current_timestamp()
        if current_time <= max_timestamp_overall:
            # Clock has gone backwards or not advanced enough
            # Set offset so we continue from where we left off
            self._clock_offset = max_timestamp_overall - current_time + 1
            print(f"[IDGenerator] Clock regression detected. Applied offset: +{self._clock_offset}ms")
    
    def _current_timestamp(self) -> int:
        """Get current timestamp in milliseconds since custom epoch.
        
        Returns:
            Milliseconds since EPOCH_START, plus any clock offset
        """
        unix_ms = int(time.time() * 1000)
        custom_epoch_ms = unix_ms - EPOCH_START + self._clock_offset
        
        # Ensure timestamp doesn't overflow our 42-bit limit
        if custom_epoch_ms > MAX_TIMESTAMP:
            raise OverflowError(f"Timestamp overflow: {custom_epoch_ms} exceeds {MAX_TIMESTAMP}")
        
        return custom_epoch_ms
    
    def _extract_timestamp(self, id_val: int) -> int:
        """Extract timestamp from an ID."""
        return (id_val >> TIMESTAMP_SHIFT) & MAX_TIMESTAMP
    
    def _extract_entity_type(self, id_val: int) -> int:
        """Extract entity type from an ID."""
        return (id_val >> ENTITY_TYPE_SHIFT) & MAX_ENTITY_TYPE
    
    def _extract_sequence(self, id_val: int) -> int:
        """Extract sequence number from an ID."""
        return (id_val >> SEQUENCE_SHIFT) & MAX_SEQUENCE
    
    def _generate_id(self, entity_type: int) -> int:
        """Generate a new unique ID for the given entity type.
        
        Args:
            entity_type: One of ENTITY_TYPE_* constants
            
        Returns:
            A unique 64-bit integer ID
            
        Raises:
            ValueError: If entity_type is invalid
            RuntimeError: If sequence overflow occurs (>4096 IDs in same millisecond)
        """
        if entity_type not in self._locks:
            raise ValueError(f"Invalid entity_type: {entity_type}")
        
        with self._locks[entity_type]:
            timestamp = self._current_timestamp()
            
            # If timestamp hasn't advanced, increment sequence
            if timestamp == self._last_timestamp[entity_type]:
                self._sequence[entity_type] = (self._sequence[entity_type] + 1) & MAX_SEQUENCE
                
                # Sequence overflow - wait for next millisecond
                if self._sequence[entity_type] == 0:
                    # We've exhausted all 4096 IDs in this millisecond
                    # Wait until clock advances
                    while timestamp <= self._last_timestamp[entity_type]:
                        timestamp = self._current_timestamp()
            else:
                # New timestamp, reset sequence
                self._sequence[entity_type] = 0
            
            # Update state
            self._last_timestamp[entity_type] = timestamp
            
            # Pack the ID: | timestamp (42) | entity_type (10) | sequence (12) |
            id_val = (
                (timestamp << TIMESTAMP_SHIFT) |
                (entity_type << ENTITY_TYPE_SHIFT) |
                (self._sequence[entity_type] << SEQUENCE_SHIFT)
            )
            
            return id_val
    
    def next_ship_id(self) -> int:
        """Generate a unique ID for a ship.
        
        Returns:
            A unique 64-bit integer ID for a ship
        """
        return self._generate_id(ENTITY_TYPE_SHIP)
    
    def next_item_id(self) -> int:
        """Generate a unique ID for an item.
        
        Returns:
            A unique 64-bit integer ID for an item
        """
        return self._generate_id(ENTITY_TYPE_ITEM)
    
    def next_player_id(self) -> int:
        """Generate a unique ID for a player.
        
        Returns:
            A unique 64-bit integer ID for a player
        """
        return self._generate_id(ENTITY_TYPE_PLAYER)
    
    def next_faction_id(self) -> int:
        """Generate a unique ID for a faction.
        
        Returns:
            A unique 64-bit integer ID for a faction
        """
        return self._generate_id(ENTITY_TYPE_FACTION)
    
    def get_clock_offset(self) -> int:
        """Get the current clock offset in milliseconds.
        
        Returns:
            Clock offset applied to timestamps (0 if no offset)
        """
        return self._clock_offset
