# Aidan Orion 23 Feb 2026
# The actions for the game
# This module handles tick-based game actions that are queued and executed in order.
# Non-tick actions (trading, quests) should be implemented separately.

from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
from threading import Lock

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
        """Iterate through all real nodes (skipping sentinels)."""
        current = self.head.next
        while current != self.tail:
            yield current
            current = current.next
    
    def clear(self):
        """Clear the list by reconnecting head and tail."""
        self.head.next = self.tail
        self.tail.prev = self.head


# ============================================================================
# ACTION QUEUES (cleared each tick)
# ============================================================================
# Per tick, actions are queued by type and executed in order: attack -> move -> collect

# Five action lists (one per action type)
attack_ship_list = ActionList('attack_ship')
attack_ship_component_list = ActionList('attack_ship_component')
attack_item_list = ActionList('attack_item')
move_list = ActionList('move')
collect_list = ActionList('collect')

# Map action type to list for easy lookup
action_type_to_list: Dict[str, ActionList] = {
    'attack_ship': attack_ship_list,
    'attack_ship_component': attack_ship_component_list,
    'attack_item': attack_item_list,
    'move': move_list,
    'collect': collect_list,
}

# Ship ID -> ActionNode (for O(1) lookup and updates)
ship_to_node: Dict[int, ActionNode] = {}

# Node pool for reuse (ship_id -> ActionNode)
node_pool: Dict[int, ActionNode] = {}


def queue_action(ship_id: int, action: str, target, target_data: Optional[str] = None, action_hash: Optional[str] = None) -> bool:
    """Queue an action to be executed on the next tick.
    
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
    if action not in action_type_to_list:
        return False
    
    # Special validation for attack_ship_component
    if action == 'attack_ship_component' and target_data is None:
        return False  # Component slot is required
    
    # Get or create node for this ship
    if ship_id in ship_to_node:
        node = ship_to_node[ship_id]
        
        # Check if action is identical (spam protection)
        if action_hash is not None and node.action_hash == action_hash:
            return True  # Same action, do nothing
        
        # Action changed - remove from current list
        # We don't need to know which list it's in - just remove it locally
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
        
        ship_to_node[ship_id] = node
    
    # Append to the appropriate list
    target_list = action_type_to_list[action]
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
    
    Clears the linked lists but keeps nodes in the pool for reuse.
    """
    attack_ship_list.clear()
    attack_ship_component_list.clear()
    attack_item_list.clear()
    move_list.clear()
    collect_list.clear()
    
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


# ============================================================================
# ACTIONS (executed during tick processing)
# ============================================================================

def attack_ship(attacker_id: int, target_ship_id: int) -> bool:
    """Attack another ship's HP (must be at same location).
    
    Damage is applied in this order:
    1. Check shield pool first - if shields exist, they absorb damage
    2. If shields are depleted or don't exist, damage goes to ship HP
    
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
        
        # Get attacker's weapon damage
        damage = get_ship_weapon_damage(attacker_id)
        
        if damage <= 0:
            return False  # No weapon or no damage
        
        # Check shield pool first
        current_shield = target_ship.get('shield_pool', 0.0)
        
        if current_shield > 0:
            # Shields absorb damage first
            shield_result = dh.damage_shield_pool(target_ship_id, damage)
            overflow_damage = shield_result['overflow_damage']
            
            # If there's overflow damage, apply it to ship HP
            if overflow_damage > 0:
                dh.damage_ship_hp(target_ship_id, overflow_damage)
        else:
            # No shields, damage goes directly to HP
            dh.damage_ship_hp(target_ship_id, damage)
        
        return True
        
    except (KeyError, ValueError):
        return False


def attack_ship_component(attacker_id: int, target_ship_id: int, component_slot: str) -> bool:
    """Attack a specific component on another ship (must be at same location).
    
    Damage is applied in this order:
    1. Check shield pool first - if shields exist, they absorb damage
    2. If shields are depleted or don't exist, damage goes to the component
    
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
        
        # Get the component ID from the ship
        component_id = target_ship.get(component_slot)
        
        if component_id is None or not isinstance(component_id, int):
            return False  # No component equipped in that slot
        
        # Get attacker's weapon damage
        damage = get_ship_weapon_damage(attacker_id)
        
        if damage <= 0:
            return False  # No weapon or no damage
        
        # Check shield pool first
        current_shield = target_ship.get('shield_pool', 0.0)
        
        if current_shield > 0:
            # Shields absorb damage first
            shield_result = dh.damage_shield_pool(target_ship_id, damage)
            overflow_damage = shield_result['overflow_damage']
            
            # If there's overflow damage, apply it to the component
            if overflow_damage > 0:
                dh.damage_item(component_id, overflow_damage)
        else:
            # No shields, damage goes directly to component
            dh.damage_item(component_id, damage)
        
        return True
        
    except (KeyError, ValueError):
        return False


def attack_item(attacker_id: int, target_item_id: int) -> bool:
    """Attack an item at a location (attacker must be at same location as item).
    
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
        # Verify ship and destination exist
        _ = dh.get_ship(ship_id)
        dest_location = dh.get_location(destination)
        
        # Get current location (O(1) lookup)
        current_location_name = get_ship_location(ship_id)
        if current_location_name is None:
            return False
        
        current_location = dh.get_location(current_location_name)
        
        # Verify locations are linked
        if destination not in current_location.get('links', []):
            return False
        
        # Use thread-safe move method
        dh.move_ship_between_locations(ship_id, current_location_name, destination)
        
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
        # Verify ship and item exist
        _ = dh.get_ship(collector_id)
        _ = dh.get_item(item_id)
        
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
        dh.transfer_item_location_to_ship(item_id, ship_location, collector_id)
        
        return True
        
    except (KeyError, ValueError):
        return False


# ============================================================================
# TICK PROCESSING
# ============================================================================

def process_tick() -> Dict[str, int]:
    """Process all queued actions in order: attacks (all types) -> move -> collect.
    
    Actions are executed in the order they were queued (FIFO within each action type).
    
    Returns a summary of actions executed.
    
    Returns:
        Dict with counts of successful actions: {
            'attack_ship': n,
            'attack_ship_component': n,
            'attack_item': n,
            'moves': n,
            'collects': n
        }
    """
    dh = _get_data_handler()
    
    # Clear locks from previous tick
    dh.clear_locks()
    
    stats = {
        'attack_ship': 0,
        'attack_ship_component': 0,
        'attack_item': 0,
        'moves': 0,
        'collects': 0
    }
    
    # Phase 1a: Process ship attacks (in order)
    for node in attack_ship_list.iterate():
        if attack_ship(node.ship_id, node.target):
            stats['attack_ship'] += 1
    
    # Phase 1b: Process ship component attacks (in order)
    for node in attack_ship_component_list.iterate():
        if attack_ship_component(node.ship_id, node.target, node.target_data):
            stats['attack_ship_component'] += 1
    
    # Phase 1c: Process item attacks (in order)
    for node in attack_item_list.iterate():
        if attack_item(node.ship_id, node.target):
            stats['attack_item'] += 1
    
    # Phase 2: Process moves (in order)
    for node in move_list.iterate():
        if move(node.ship_id, node.target):
            stats['moves'] += 1
    
    # Phase 3: Process collects (in order)
    for node in collect_list.iterate():
        if collect(node.ship_id, node.target):
            stats['collects'] += 1
    
    # Clear queues for next tick
    clear_queues()
    
    return stats


# ============================================================================
# ACTION DELEGATOR (legacy support)
# ============================================================================

def doaction(ship_id: int, action: str, target, target_data: Optional[str] = None, action_hash: Optional[str] = None) -> bool:
    """Queue an action to be executed on next tick (legacy interface).
    
    Args:
        ship_id: Ship performing the action
        action: Action type ('attack_ship', 'attack_ship_component', 'attack_item', 'move', or 'collect')
        target: Target for the action
        target_data: Additional data (e.g., component slot for attack_ship_component)
        action_hash: Hash from client to detect duplicate actions
        
    Returns:
        True if action was queued successfully
    """
    return queue_action(ship_id, action, target, target_data, action_hash)


actionhandler = {
    'attack_ship': lambda ship_id, target, action_hash=None: queue_action(ship_id, 'attack_ship', target, None, action_hash),
    'attack_ship_component': lambda ship_id, target, component_slot, action_hash=None: queue_action(ship_id, 'attack_ship_component', target, component_slot, action_hash),
    'attack_item': lambda ship_id, target, action_hash=None: queue_action(ship_id, 'attack_item', target, None, action_hash),
    'move': lambda ship_id, target, action_hash=None: queue_action(ship_id, 'move', target, None, action_hash),
    'collect': lambda ship_id, target, action_hash=None: queue_action(ship_id, 'collect', target, None, action_hash),
}


__all__ = [
    'doaction',
    'actionhandler',
    'queue_action',
    'process_tick',
    'clear_queues',
    'attack_ship',
    'attack_ship_component',
    'attack_item',
    'ActionNode',
    'ActionList',
    'ship_to_node',
    'node_pool',
]
