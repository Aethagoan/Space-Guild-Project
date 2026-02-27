# Aidan Orion 23 Feb 2026
# The actions for the game
# This module handles tick-based game actions that are queued and executed in order.
# Non-tick actions (trading, quests) should be implemented separately.

from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import will happen at runtime to avoid circular imports
# Access via: from program import data_handler
data_handler = None

def _get_data_handler():
    """Lazy import to avoid circular dependency."""
    global data_handler
    if data_handler is None:
        from program import data_handler as dh
        data_handler = dh
    return data_handler


def _set_data_handler(handler):
    """Set the data handler instance for testing purposes.
    
    Args:
        handler: DataHandler instance to use
    """
    global data_handler
    data_handler = handler


# ============================================================================
# ACTION NODE AND LINKED LIST IMPLEMENTATION
# ============================================================================

class ActionNode:
    """Node in the action queue linked list.
    
    Each ship gets one node that can be reused between ticks and moved between lists.
    """
    def __init__(self, ship_id: int):
        self.ship_id = ship_id
        self.action_type: Optional[str] = None
        self.target: Any = None
        self.target_data: Optional[Any] = None
        self.action_hash: Optional[str] = None
        self.prev: Optional['ActionNode'] = None
        self.next: Optional['ActionNode'] = None
        self._lock = Lock()
    
    def update_action(self, action_type: str, target: Any, target_data: Optional[Any], action_hash: Optional[str]):
        """Update this node's action data."""
        self.action_type = action_type
        self.target = target
        self.target_data = target_data
        self.action_hash = action_hash


class ActionList:
    """Doubly-linked list with sentinel head and tail nodes.
    
    Real action nodes are always between head and tail.
    This ensures uniform removal logic with no edge cases.
    """
    def __init__(self, name: str):
        self.name = name
        # Sentinel nodes (ship_id = -1 means not a real ship)
        self.head = ActionNode(-1)
        self.tail = ActionNode(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def append(self, node: ActionNode):
        """Append node to the tail of the list.
        
        Locks the tail's prev node and the tail itself during modification.
        """
        # Lock the nodes we're modifying
        with self.tail._lock, self.tail.prev._lock:
            node.prev = self.tail.prev
            node.next = self.tail
            self.tail.prev.next = node
            self.tail.prev = node
    
    def remove(self, node: ActionNode):
        """Remove node from the list.
        
        Locks the node's neighbors during modification.
        Works uniformly regardless of node position due to sentinel nodes.
        """
        # Lock the neighbors we're modifying
        with node.prev._lock, node.next._lock:
            node.prev.next = node.next
            node.next.prev = node.prev
        # Don't clear node.prev/next - might reuse them for debugging
    
    def iterate(self):
        """Iterate through all real nodes (skipping sentinels).
        
        Yields:
            ActionNode: Real action nodes (not sentinels)
        """
        current: ActionNode = self.head.next  # type: ignore - sentinel.next is always ActionNode
        while current != self.tail:
            yield current
            current = current.next  # type: ignore - during iteration, next is always valid
    
    def clear(self):
        """Clear the list by reconnecting head and tail."""
        self.head.next = self.tail
        self.tail.prev = self.head


# ============================================================================
# STEALTH NODE AND LINKED LIST IMPLEMENTATION
# ============================================================================

class StealthNode:
    """Node in the active stealth linked list.
    
    Tracks ships with active stealth cloaks and their remaining duration.
    """
    def __init__(self, ship_id: int, duration_ticks: int):
        self.ship_id = ship_id
        self.remaining_ticks = duration_ticks
        self.prev: Optional['StealthNode'] = None
        self.next: Optional['StealthNode'] = None
        self._lock = Lock()


class StealthList:
    """Doubly-linked list for active stealth ships with sentinel nodes."""
    def __init__(self):
        # Sentinel nodes (ship_id = -1 means not a real ship)
        self.head = StealthNode(-1, 0)
        self.tail = StealthNode(-1, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def append(self, node: StealthNode):
        """Append node to the tail of the list."""
        with self.tail._lock, self.tail.prev._lock:
            node.prev = self.tail.prev
            node.next = self.tail
            self.tail.prev.next = node
            self.tail.prev = node
    
    def remove(self, node: StealthNode):
        """Remove node from the list."""
        with node.prev._lock, node.next._lock:
            node.prev.next = node.next
            node.next.prev = node.prev
    
    def iterate(self):
        """Iterate through all real nodes (skipping sentinels)."""
        current: StealthNode = self.head.next  # type: ignore
        while current != self.tail:
            yield current
            current = current.next  # type: ignore


# ============================================================================
# STEALTH TRACKING (persists across ticks)
# ============================================================================

# Active stealth ships (persists across ticks)
active_stealth_list = StealthList()

# Ship ID -> StealthNode for O(1) lookup
active_stealth: Dict[int, StealthNode] = {}

# Ships that took damage this tick - can't activate stealth (cleared each tick)
stealth_disabled: set[int] = set()


# ============================================================================
# ACTION QUEUES (cleared each tick)
# ============================================================================
# MULTI-THREADED ARCHITECTURE:
# Actions are organized by LOCATION to enable parallel processing per location.
# Each location is processed in its own thread during tick execution.
# 
# Per tick execution order within each location thread:
#   1. All scans (scan ship, scan item, scan location)
#   2. All attacks (attack_ship, attack_ship_component, attack_item)
#   3. All moves
#   4. All collects
#   5. All stealth activation and deactivation


location_queues: Dict[str, Dict[str, ActionList]] = defaultdict(lambda: {
    'scan': ActionList('scan'),
    'attack_ship': ActionList('attack_ship'),
    'attack_ship_component': ActionList('attack_ship_component'),
    'attack_item': ActionList('attack_item'),
    'move': ActionList('move'),
    'collect': ActionList('collect'),
    'activate_stealth': ActionList('activate_stealth'),
    'deactivate_stealth': ActionList('deactivate_stealth'),
})

# Ship ID -> (ActionNode, location_name) for O(1) lookup and updates
ship_to_node: Dict[int, Tuple[ActionNode, str]] = {}

# Node pool for reuse (ship_id -> ActionNode)
node_pool: Dict[int, ActionNode] = {}


def queue_action(ship_id: int, action: str, target, target_data: Optional[str] = None, action_hash: Optional[str] = None) -> bool:
    """Queue an action to be executed on the next tick.
    
    Actions are organized by LOCATION to support multi-threaded tick processing.
    Each location's actions will be processed in a separate thread.
    
    If the ship already has an action queued:
    - If action_hash matches: do nothing (spam protection)
    - If action changed: remove from old list, update node, append to new list
    
    Args:
        ship_id: ID of the ship performing the action
        action: Action type ('attack_ship', 'attack_ship_component', 'attack_item', 'move', or 'collect')
        target: Target for the action (ship_id/item_id for attacks, location_name for move, item_id for collect)
        target_data: Additional data for certain actions (e.g., component slot for attack_ship_component)
        action_hash: Hash from client to detect if action truly changed (optional)
        
    Returns:
        True if action was queued successfully, False if action type is invalid
    """
    # Validate action type
    valid_actions = {'scan', 'attack_ship', 'attack_ship_component', 'attack_item', 'move', 'collect', 'activate_stealth', 'deactivate_stealth'}
    if action not in valid_actions:
        return False
    
    # Special validation for attack_ship_component
    if action == 'attack_ship_component' and target_data is None:
        return False  # Component slot is required
    
    # Get ship's current location - required to queue action in correct location bucket
    ship_location = get_ship_location(ship_id)
    if ship_location is None:
        return False  # Ship doesn't exist or has no location
    
    # Get or create node for this ship
    if ship_id in ship_to_node:
        node, old_location = ship_to_node[ship_id]
        
        # Check if action is identical (spam protection)
        if action_hash is not None and node.action_hash == action_hash:
            return True  # Same action, do nothing
        
        # Action changed - remove from old list in old location
        remove_node_from_list(node)
        
        # Update node data
        node.update_action(action, target, target_data, action_hash)
    else:
        # Get node from pool or create new one
        if ship_id in node_pool:
            node = node_pool[ship_id]
            node.update_action(action, target, target_data, action_hash)
        else:
            node = ActionNode(ship_id)
            node.update_action(action, target, target_data, action_hash)
            node_pool[ship_id] = node
    
    # Update ship-to-node mapping with current location
    ship_to_node[ship_id] = (node, ship_location)
    
    # Append to the appropriate location's action list
    target_list = location_queues[ship_location][action]
    target_list.append(node)
    
    return True


def remove_node_from_list(node: ActionNode):
    """Remove a node from whatever list it's in.
    
    This works uniformly due to sentinel nodes - we don't need to know which list.
    """
    with node.prev._lock, node.next._lock:
        node.prev.next = node.next
        node.next.prev = node.prev


def clear_queues():
    """Clear all action queues. Called after tick execution.
    
    Clears all location-based linked lists but keeps nodes in the pool for reuse.
    """
    # Clear all action lists for all locations
    for location_name, action_lists in location_queues.items():
        for action_type, action_list in action_lists.items():
            action_list.clear()
    
    # Clear the location queues dictionary
    location_queues.clear()
    
    # Clear the ship-to-node mapping (but keep nodes in pool)
    ship_to_node.clear()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_ship_location(ship_id: int) -> Optional[str]:
    """Get the location of a ship (O(1) lookup from ship's location field).
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Location name if ship exists, None if ship doesn't exist
    """
    dh = _get_data_handler()
    try:
        return dh.get_ship_location(ship_id)
    except KeyError:
        return None


def can_fit_item(ship_id: int, item_id: int) -> bool:
    """Check if an item can fit in a ship's cargo.
    
    Args:
        ship_id: Ship ID
        item_id: Item ID to check
        
    Returns:
        True if item fits, False otherwise
    """
    from components import can_fit_item_in_cargo
    return can_fit_item_in_cargo(ship_id, item_id)


def _spill_cargo_to_location(ship_id: int, location_name: str) -> None:
    """Spill all items from a ship's cargo to a location when cargo is destroyed.
    
    Args:
        ship_id: Ship ID whose cargo was destroyed
        location_name: Location to spill items to
    """
    dh = _get_data_handler()
    
    try:
        ship = dh.get_ship(ship_id)
        items_to_spill = ship['items'].copy()
        
        # Move each item from ship's cargo to the location using thread-safe method
        for item_id in items_to_spill:
            try:
                dh.move_item_ship_to_location(item_id, ship_id, location_name)
            except (KeyError, ValueError):
                # Item doesn't exist or other error - skip it
                pass
        
    except KeyError:
        # Ship doesn't exist - nothing to spill
        pass


def is_ship_stealthed(ship_id: int) -> bool:
    """Check if a ship currently has active stealth (O(1) lookup).
    
    Args:
        ship_id: Ship ID to check
        
    Returns:
        True if ship has active stealth, False otherwise
    """
    return ship_id in active_stealth


def is_safe_zone(location_name: str) -> bool:
    """Check if a location is a safe zone where weapons are disabled.
    
    Safe zones have the 'Safe' tag in their tags list.
    
    Args:
        location_name: Location name to check
        
    Returns:
        True if location is a safe zone (weapons disabled), False otherwise
    """
    dh = _get_data_handler()
    try:
        location = dh.get_location(location_name)
        tags = location.get('tags', [])
        return 'Safe' in tags
    except KeyError:
        # Location doesn't exist - default to not safe
        return False


def activate_stealth(ship_id: int) -> bool:
    """Activate stealth cloak for a ship.
    
    Duration is calculated as: floor(5 * (1 + tier) * multiplier) ticks
    
    Args:
        ship_id: Ship ID
        
    Returns:
        True if stealth activated successfully, False otherwise
    """
    from components import get_ship_stealth_cloak
    dh = _get_data_handler()
    
    try:
        # Check if stealth is disabled (took damage this tick)
        if ship_id in stealth_disabled:
            return False
        
        # Check if already stealthed
        if ship_id in active_stealth:
            return False
        
        # Get stealth cloak component
        stealth_cloak = get_ship_stealth_cloak(ship_id)
        if stealth_cloak is None:
            return False
        
        # Check health
        health = stealth_cloak['health']
        if health <= 0:
            return False
        
        # Calculate duration: floor(5 * (1 + tier) * multiplier)
        tier = stealth_cloak['tier']
        multiplier = stealth_cloak['multiplier']
        duration = int(5 * (1 + tier) * multiplier)
        
        if duration <= 0:
            return False
        
        # Create stealth node and add to list
        node = StealthNode(ship_id, duration)
        active_stealth_list.append(node)
        active_stealth[ship_id] = node
        
        return True
        
    except (KeyError, ValueError):
        return False


def deactivate_stealth(ship_id: int) -> bool:
    """Deactivate stealth for a ship (manual or forced).
    
    Args:
        ship_id: Ship ID
        
    Returns:
        True if stealth was deactivated, False if not stealthed
    """
    if ship_id not in active_stealth:
        return False
    
    # Remove from list and dictionary
    node = active_stealth[ship_id]
    active_stealth_list.remove(node)
    del active_stealth[ship_id]
    
    return True


def mark_ship_took_damage(ship_id: int) -> None:
    """Mark that a ship took damage - disables stealth activation and deactivates if active.
    
    This is called when a ship takes damage. The stealth_disabled flag is cleared
    at the end of the tick.
    
    Args:
        ship_id: Ship ID that took damage
    """
    # Add to disabled set
    stealth_disabled.add(ship_id)
    
    # Deactivate stealth if currently active
    deactivate_stealth(ship_id)


# ============================================================================
# ACTIONS (executed during tick processing)
# ============================================================================

def attack_ship(attacker_id: int, target_ship_id: int) -> bool:
    """Attack another ship's HP (must be at same location).
    
    Damage is applied in this order:
    1. Check shield pool first - if shields exist, they absorb damage
    2. If shields are depleted or don't exist, damage goes to ship HP
    
    Weapons are disabled in safe zones (locations with 'Safe' tag).
    
    Args:
        attacker_id: Attacking ship ID
        target_ship_id: Target ship ID
        
    Returns:
        True if attack was successful, False otherwise
    """
    dh = _get_data_handler()
    
    try:
        # Import components module for damage calculation
        from components import get_ship_weapon_damage
        
        # Verify both ships exist
        _ = dh.get_ship(attacker_id)
        target_ship = dh.get_ship(target_ship_id)
        
        # Get locations (O(1) lookups)
        attacker_location = get_ship_location(attacker_id)
        target_location = get_ship_location(target_ship_id)
        
        # Ships must be at same location
        if attacker_location is None or attacker_location != target_location:
            return False
        
        # Check if location is a safe zone (weapons disabled)
        if is_safe_zone(attacker_location):
            return False
        
        # Get attacker's weapon damage
        damage = get_ship_weapon_damage(attacker_id)
        
        if damage <= 0:
            return False  # No weapon or no damage
        
        # Attacking deactivates stealth
        deactivate_stealth(attacker_id)
        
        # Apply damage - shields absorb first, overflow goes to HP
        shield_result = dh.damage_shield_pool(target_ship_id, damage)
        overflow_damage = shield_result['overflow_damage']
        
        # If there's overflow damage, apply it to ship HP
        if overflow_damage > 0:
            dh.damage_ship_hp(target_ship_id, overflow_damage)
            # Mark that ship took damage (disables stealth)
            mark_ship_took_damage(target_ship_id)
        elif shield_result['shield_damage'] > 0:
            # Shields absorbed some/all damage but didn't break - still counts as taking damage
            mark_ship_took_damage(target_ship_id)
        
        return True
        
    except (KeyError, ValueError):
        return False


def attack_ship_component(attacker_id: int, target_ship_id: int, component_slot: str) -> bool:
    """Attack a specific component slot on a target ship (ships must be at same location).
    
    Weapons are disabled in safe zones - attacks cannot be made from locations tagged as 'Safe'.
    
    Damage is applied in this order:
    1. Check shield pool first - if shields exist, they absorb damage
    2. If shields are depleted:
       - If component exists in slot, damage goes to the component
       - If component slot is empty, deal 5x critical damage directly to ship HP
    
    Args:
        attacker_id: Attacking ship ID
        target_ship_id: Target ship ID
        component_slot: Component slot to damage ('engine_id', 'weapon_id', 'shield_id', 
                       'cargo_id', 'sensor', 'stealth_cloak_id')
        
    Returns:
        True if attack was successful, False otherwise
    """
    dh = _get_data_handler()
    
    try:
        # Import components module for damage calculation
        from components import get_ship_weapon_damage
        
        # Verify component slot is valid
        valid_components = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor', 'stealth_cloak_id']
        if component_slot not in valid_components:
            return False  # Invalid component target
        
        # Verify both ships exist
        _ = dh.get_ship(attacker_id)
        target_ship = dh.get_ship(target_ship_id)
        
        # Get locations (O(1) lookups)
        attacker_location = get_ship_location(attacker_id)
        target_location = get_ship_location(target_ship_id)
        
        # Ships must be at same location
        if attacker_location is None or attacker_location != target_location:
            return False
        
        # Check if attacker is in a safe zone (weapons disabled)
        if is_safe_zone(attacker_location):
            return False
        
        # Get the component ID from the ship
        component_id = target_ship.get(component_slot)
        
        # Get attacker's weapon damage
        damage = get_ship_weapon_damage(attacker_id)
        
        if damage <= 0:
            return False  # No weapon or no damage
        
        # Attacking deactivates stealth
        deactivate_stealth(attacker_id)
        
        # Apply damage - shields absorb first, overflow goes to component or HP
        shield_result = dh.damage_shield_pool(target_ship_id, damage)
        overflow_damage = shield_result['overflow_damage']
        
        # If there's overflow damage after shields
        if overflow_damage > 0:
            # Check if component slot is empty (critical hit)
            if component_id is None or not isinstance(component_id, int):
                # CRITICAL HIT: Empty component slot with shields down = 5x damage to ship HP
                critical_damage = overflow_damage * 5.0
                dh.damage_ship_hp(target_ship_id, critical_damage)
                # Mark that ship took damage (disables stealth)
                mark_ship_took_damage(target_ship_id)
            else:
                # Normal: overflow damage goes to component
                damage_result = dh.damage_item(component_id, overflow_damage)
                
                # If cargo was disabled, spill all items to location
                if damage_result['disabled'] and component_slot == 'cargo_id' and target_location is not None:
                    _spill_cargo_to_location(target_ship_id, target_location)
        
        return True
        
    except (KeyError, ValueError):
        return False


def attack_item(attacker_id: int, target_item_id: int) -> bool:
    """Attack an item at a location (attacker must be at same location as item).
    
    Weapons are disabled in safe zones - attacks cannot be made from locations tagged as 'Safe'.
    
    Items don't have shields, so damage goes directly to the item's health.
    When an item's health reaches 0, its multiplier is set to 0 (destroyed).
    
    Args:
        attacker_id: Attacking ship ID
        target_item_id: Target item ID
        
    Returns:
        True if attack was successful, False otherwise
    """
    dh = _get_data_handler()
    
    try:
        # Import components module for damage calculation
        from components import get_ship_weapon_damage
        
        # Verify ship and item exist
        _ = dh.get_ship(attacker_id)
        _ = dh.get_item(target_item_id)
        
        # Get attacker's location (O(1) lookup)
        attacker_location = get_ship_location(attacker_id)
        
        if attacker_location is None:
            return False
        
        # Verify item is at the same location
        location = dh.get_location(attacker_location)
        if target_item_id not in location.get('items', []):
            return False  # Item is not at this location
        
        # Check if attacker is in a safe zone (weapons disabled)
        if is_safe_zone(attacker_location):
            return False
        
        # Get attacker's weapon damage
        damage = get_ship_weapon_damage(attacker_id)
        
        if damage <= 0:
            return False  # No weapon or no damage
        
        # Apply damage directly to item (items don't have shields)
        dh.damage_item(target_item_id, damage)
        
        return True
        
    except (KeyError, ValueError):
        return False


def move(ship_id: int, destination: str) -> bool:
    """Move a ship to a linked location.
    
    Args:
        ship_id: Ship ID to move
        destination: Destination location name
        
    Returns:
        True if move was successful, False otherwise
    """
    dh = _get_data_handler()
    
    try:
        # Import components module
        from components import get_ship_engine
        
        # Verify ship and destination exist
        _ = dh.get_ship(ship_id)
        dest_location = dh.get_location(destination)
        
        # Check if engine exists and has health > 0
        engine = get_ship_engine(ship_id)
        if engine is None:
            return False  # No engine equipped
        
        engine_health = engine['health']
        if engine_health <= 0:
            return False  # Engine is destroyed - can't move
        
        # Get current location (O(1) lookup)
        current_location_name = get_ship_location(ship_id)
        if current_location_name is None:
            return False
        
        current_location = dh.get_location(current_location_name)
        
        # Verify locations are linked
        if destination not in current_location.get('links', []):
            return False
        
        # Check if ship is stealthed and add engine trail log
        was_stealthed = is_ship_stealthed(ship_id)
        if was_stealthed:
            # Add log to current location about energy signatures
            ship = dh.get_ship(ship_id)
            ship_name = ship.get('name', f'Ship {ship_id}')
            current_location['logs'].append(f"Faint energy signatures detected from {ship_name} departing toward {destination}.")
        
        # Use thread-safe move method
        dh.move_ship_between_locations(ship_id, current_location_name, destination)
        
        # Disable stealth if entering a station or starport
        dest_type = dest_location.get('type', 'space')
        if dest_type in ['station', 'starport']:
            deactivate_stealth(ship_id)
        
        return True
        
    except (KeyError, ValueError):
        return False


def collect(collector_id: int, item_id: int) -> bool:
    """Collect an item from the current location into ship cargo.
    
    Args:
        collector_id: Collecting ship ID
        item_id: Item ID to collect
        
    Returns:
        True if collection was successful, False otherwise
    """
    dh = _get_data_handler()
    
    try:
        # Import components module
        from components import get_ship_cargo
        
        # Verify ship and item exist
        ship = dh.get_ship(collector_id)
        _ = dh.get_item(item_id)
        
        # Check if cargo exists and has health > 0
        cargo = get_ship_cargo(collector_id)
        if cargo is None:
            return False  # No cargo equipped
        
        cargo_health = cargo['health']
        if cargo_health <= 0:
            return False  # Cargo is destroyed - can't pick up items
        
        # Get ship's location (O(1) lookup)
        ship_location = get_ship_location(collector_id)
        if ship_location is None:
            return False
        
        location = dh.get_location(ship_location)
        
        # Verify item is at this location
        if item_id not in location.get('items', []):
            return False
        
        # Check cargo capacity
        if not can_fit_item(collector_id, item_id):
            return False
        
        # Use thread-safe transfer method
        dh.move_item_location_to_ship(item_id, ship_location, collector_id)
        
        return True
        
    except (KeyError, ValueError):
        return False


def scan_ship(scanner_id: int, target_ship_id: int) -> Optional[Dict[str, Any]]:
    """Scan another ship to reveal all its information.
    
    Ships must be at the same location. Returns full ship data including HP, 
    components, cargo, and all other stats. Scan results are not persisted in 
    the backend - they're returned once and the client manages caching.
    
    Args:
        scanner_id: Scanning ship ID
        target_ship_id: Target ship ID to scan
        
    Returns:
        Dict with full ship data if successful, None if scan failed
    """
    dh = _get_data_handler()
    
    try:
        # Import components module
        from components import get_ship_sensor
        
        # Verify both ships exist
        scanner_ship = dh.get_ship(scanner_id)
        target_ship = dh.get_ship(target_ship_id)
        
        # Check if scanner has a sensor with health > 0
        sensor = get_ship_sensor(scanner_id)
        if sensor is None:
            return None  # No sensor equipped
        
        sensor_health = sensor['health']
        if sensor_health <= 0:
            return None  # Sensor is destroyed - can't scan
        
        # Get locations (O(1) lookups)
        scanner_location = get_ship_location(scanner_id)
        target_location = get_ship_location(target_ship_id)
        
        # Ships must be at same location
        if scanner_location is None or scanner_location != target_location:
            return None
        
        # Check if target has active stealth
        if is_ship_stealthed(target_ship_id):
            # Ship is stealthed - hidden from scans
            return None
        
        # Log the scan event to location
        dh.add_location_log(scanner_location, {
            'type': 'scan',
            'content': f'ship:{scanner_id} scanned ship:{target_ship_id}',
            'scanner': f'ship:{scanner_id}',
            'target': f'ship:{target_ship_id}'
        })
        
        # Notify the target ship that it was scanned
        dh.add_ship_log(target_ship_id, {
            'type': 'computer',
            'content': f'Scanned by ship:{scanner_id}',
            'source': f'ship:{scanner_id}'
        })
        
        # Return full ship data (copy to avoid reference issues)
        return dict(target_ship)
        
    except (KeyError, ValueError):
        return None


def scan_item(scanner_id: int, target_item_id: int) -> Optional[Dict[str, Any]]:
    """Scan an item at a location to reveal all its information.
    
    Scanner must be at same location as the item. Returns full item data.
    
    Args:
        scanner_id: Scanning ship ID
        target_item_id: Target item ID to scan
        
    Returns:
        Dict with full item data if successful, None if scan failed
    """
    dh = _get_data_handler()
    
    try:
        # Import components module
        from components import get_ship_sensor
        
        # Verify ship and item exist
        _ = dh.get_ship(scanner_id)
        target_item = dh.get_item(target_item_id)
        
        # Check if scanner has a sensor with health > 0
        sensor = get_ship_sensor(scanner_id)
        if sensor is None:
            return None  # No sensor equipped
        
        sensor_health = sensor['health']
        if sensor_health <= 0:
            return None  # Sensor is destroyed - can't scan
        
        # Get scanner's location (O(1) lookup)
        scanner_location = get_ship_location(scanner_id)
        if scanner_location is None:
            return None
        
        location = dh.get_location(scanner_location)
        
        # Verify item is at this location
        if target_item_id not in location.get('items', []):
            return None
        
        # Log the scan event to location
        dh.add_location_log(scanner_location, {
            'type': 'scan',
            'content': f'ship:{scanner_id} scanned item:{target_item_id}',
            'scanner': f'ship:{scanner_id}',
            'target': f'item:{target_item_id}'
        })
        
        # Return full item data (copy to avoid reference issues)
        return dict(target_item)
        
    except (KeyError, ValueError):
        return None


def scan_location(scanner_id: int, target_location_name: str) -> Optional[Dict[str, Any]]:
    """Scan a different location to reveal ships and items there.
    
    Scanner must NOT be at the target location (scan remote locations only).
    Returns location data including ship IDs and item IDs, filtered by stealth.
    
    Args:
        scanner_id: Scanning ship ID
        target_location_name: Target location name to scan
        
    Returns:
        Dict with location data if successful, None if scan failed
    """
    dh = _get_data_handler()
    
    try:
        # Import components module
        from components import get_ship_sensor
        
        # Verify ship exists
        _ = dh.get_ship(scanner_id)
        
        # Check if scanner has a sensor with health > 0
        sensor = get_ship_sensor(scanner_id)
        if sensor is None:
            return None  # No sensor equipped
        
        sensor_health = sensor['health']
        if sensor_health <= 0:
            return None  # Sensor is destroyed - can't scan
        
        # Get scanner's location
        scanner_location = get_ship_location(scanner_id)
        if scanner_location is None:
            return None
        
        # Can't scan own location (use local sensors for that)
        if scanner_location == target_location_name:
            return None
        
        # Verify target location exists
        target_location = dh.get_location(target_location_name)
        
        # Filter out ships with active stealth cloaks
        from components import get_ship_stealth_cloak
        visible_ship_ids = []
        for ship_id in target_location.get('ship_ids', []):
            try:
                # Check if ship has active stealth
                if not is_ship_stealthed(ship_id):
                    visible_ship_ids.append(ship_id)
            except KeyError:
                # Ship doesn't exist, skip
                continue
        
        # Log the scan event to scanner's location
        dh.add_location_log(scanner_location, {
            'type': 'scan',
            'content': f'ship:{scanner_id} scanned location:{target_location_name}',
            'scanner': f'ship:{scanner_id}',
            'target': f'location:{target_location_name}'
        })
        
        # Return location data with filtered ships
        return {
            'name': target_location.get('name'),
            'description': target_location.get('description'),
            'links': target_location.get('links', []),
            'ship_ids': visible_ship_ids,
            'items': target_location.get('items', [])
        }
        
    except (KeyError, ValueError):
        return None


# ============================================================================
# TICK PROCESSING (MULTI-THREADED BY LOCATION)
# ============================================================================

def _process_location_actions(location_name: str, actions: Dict[str, ActionList]) -> Dict[str, int]:
    """Process all actions for a specific location in a dedicated thread.
    
    THREAD SAFETY:
    - Each location is processed in its own thread
    - Different locations can execute concurrently without conflicts
    - Location-specific locks in data_handler ensure thread safety
    
    EXECUTION ORDER (within each location thread):
    0. All scans (scan_ship, scan_item, scan_location) - sequential
    1. All attacks (attack_ship, attack_ship_component, attack_item) - sequential
    2. All moves - sequential (moves OUT of location are concurrent across threads)
    3. All collects - sequential
    
    Args:
        location_name: Name of location being processed
        actions: Dict mapping action_type -> ActionList for this location
        
    Returns:
        Dict with counts of successful actions for this location
    """
    stats = {
        'scans': 0,
        'attack_ship': 0,
        'attack_ship_component': 0,
        'attack_item': 0,
        'moves': 0,
        'collects': 0,
        'stealth_activations': 0,
        'stealth_deactivations': 0,
        'stealth_expirations': 0  # Expirations are counted at tick level, not location level
    }
    
    # Phase 0: Process scans (in order within location)
    # Scans can target ships, items, or other locations
    for node in actions['scan'].iterate():
        if node.target is not None:
            # target_data determines scan type: 'ship', 'item', or 'location'
            scan_type = node.target_data
            result = None
            
            if scan_type == 'ship':
                result = scan_ship(node.ship_id, node.target)
            elif scan_type == 'item':
                result = scan_item(node.ship_id, node.target)
            elif scan_type == 'location':
                result = scan_location(node.ship_id, node.target)
            
            # If scan succeeded, add result to scanner's ship log
            if result is not None:
                dh = _get_data_handler()
                dh.add_ship_log(node.ship_id, {
                    'type': 'computer',
                    'content': f'Scan complete: {scan_type}:{node.target}',
                    'source': f'{scan_type}:{node.target}',
                    'scan_data': result
                })
                stats['scans'] += 1
    
    # Phase 1a: Process ship attacks (in order within location)
    for node in actions['attack_ship'].iterate():
        if node.target is not None and attack_ship(node.ship_id, node.target):
            stats['attack_ship'] += 1
    
    # Phase 1b: Process ship component attacks (in order within location)
    for node in actions['attack_ship_component'].iterate():
        if node.target is not None and node.target_data is not None:
            if attack_ship_component(node.ship_id, node.target, str(node.target_data)):
                stats['attack_ship_component'] += 1
    
    # Phase 1c: Process item attacks (in order within location)
    for node in actions['attack_item'].iterate():
        if node.target is not None and attack_item(node.ship_id, node.target):
            stats['attack_item'] += 1
    
    # Phase 2: Process moves (in order within location)
    # NOTE: Moves OUT of this location run concurrently with other location threads,
    # but moves INTO the same destination will serialize via location locks
    for node in actions['move'].iterate():
        if node.target is not None and move(node.ship_id, node.target):
            stats['moves'] += 1
    
    # Phase 3: Process collects (in order within location)
    for node in actions['collect'].iterate():
        if node.target is not None and collect(node.ship_id, node.target):
            stats['collects'] += 1
    
    # Phase 4: Process stealth deactivations (in order within location)
    for node in actions['deactivate_stealth'].iterate():
        if deactivate_stealth(node.ship_id):
            stats['stealth_deactivations'] += 1
    
    # Phase 5: Process stealth activations (in order within location)
    for node in actions['activate_stealth'].iterate():
        if activate_stealth(node.ship_id):
            stats['stealth_activations'] += 1
    
    return stats


def tick_stealth_timers() -> int:
    """Tick down all active stealth timers and remove expired ones.
    
    This runs BEFORE processing location actions, so stealth status is
    consistent throughout the tick.
    
    Returns:
        Number of stealth cloaks that expired this tick
    """
    expired_count = 0
    
    # Iterate through active stealth list
    current = active_stealth_list.head.next
    while current != active_stealth_list.tail:
        # Save next before we potentially remove this node
        next_node = current.next
        
        # Decrement timer
        current.remaining_ticks -= 1
        
        # Check if expired
        if current.remaining_ticks <= 0:
            # Remove from tracking
            active_stealth_list.remove(current)
            del active_stealth[current.ship_id]
            expired_count += 1
        
        current = next_node
    
    return expired_count


def update_all_location_visibility():
    """Update visible_ship_ids for all locations based on current stealth state.
    
    This should be called AFTER tick processing to cache the visible ships.
    This converts O(n²) API requests into O(n) once per tick.
    """
    dh = _get_data_handler()
    
    for location_name, location in dh.Locations.items():
        visible_ships = []
        for ship_id in location.get('ship_ids', []):
            # Only include ships that are not stealthed
            if not is_ship_stealthed(ship_id):
                visible_ships.append(ship_id)
        
        # Update the cached visible list
        location['visible_ship_ids'] = visible_ships


def process_tick() -> Dict[str, int]:
    """Process all queued actions with per-location multi-threading.

    Returns:
        Dict with counts of successful actions (aggregated across all locations): {
            'scans': n,
            'attack_ship': n,
            'attack_ship_component': n,
            'attack_item': n,
            'moves': n,
            'collects': n,
            'stealth_activations': n,
            'stealth_deactivations': n,
            'stealth_expirations': n
        }
    """
    dh = _get_data_handler()
    
    # Clear locks from previous tick
    dh.clear_locks()
    
    # Tick down stealth timers BEFORE processing actions
    stealth_expirations = tick_stealth_timers()
    
    # Initialize aggregate stats
    total_stats = {
        'scans': 0,
        'attack_ship': 0,
        'attack_ship_component': 0,
        'attack_item': 0,
        'moves': 0,
        'collects': 0,
        'stealth_activations': 0,
        'stealth_deactivations': 0,
        'stealth_expirations': stealth_expirations
    }
    
    # If no actions queued, still update visibility before returning
    if not location_queues:
        clear_queues()
        update_all_location_visibility()
        return total_stats
    
    # MULTI-THREADED EXECUTION: Process each location in parallel
    # ThreadPoolExecutor size = number of active locations (up to reasonable max)
    max_workers = min(len(location_queues), 32)  # Cap at 32 threads
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all location processing tasks
        future_to_location = {
            executor.submit(_process_location_actions, location, actions): location
            for location, actions in location_queues.items() # this says, execute all the actions in your action list by using the mapping handler, location.
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_location):
            location = future_to_location[future]
            try:
                location_stats = future.result()
                # Aggregate stats from all location threads
                for key in total_stats:
                    total_stats[key] += location_stats[key]
            except Exception as e:
                # Log error but continue processing other locations
                print(f"Error processing location {location}: {e}")
    
    # Clear queues for next tick
    clear_queues()
    
    # Clear stealth_disabled set (ships can activate stealth next tick)
    stealth_disabled.clear()
    
    # Update visible ship cache for ALL locations (O(n) once per tick vs O(n²) per API request)
    update_all_location_visibility()
    
    return total_stats


__all__ = [
    'queue_action',
    'process_tick',
    'clear_queues',
    'update_all_location_visibility',
    'attack_ship',
    'attack_ship_component',
    'attack_item',
    'scan_ship',
    'scan_item',
    'scan_location',
    'activate_stealth',
    'deactivate_stealth',
    'is_ship_stealthed',
    'ActionNode',
    'ActionList',
    'ship_to_node',
    'node_pool',
]
