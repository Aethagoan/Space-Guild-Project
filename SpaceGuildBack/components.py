# Aidan Orion 24 Feb 2026
# Ship components and stat calculations
# This module handles all component-related logic: damage calculations, capacity formulas, repairs, etc.

from typing import Optional, Dict
import math

# Import will happen at runtime to avoid circular imports
data_handler = None

def _get_data_handler():
    """Lazy import to avoid circular dependency."""
    global data_handler
    if data_handler is None:
        from program import data_handler as dh
        data_handler = dh
    return data_handler


def _set_data_handler(handler):
    """Set the data handler instance.
    
    Args:
        handler: DataHandler instance to use
    """
    global data_handler
    data_handler = handler


# ============================================================================
# COMPONENT GETTERS
# ============================================================================
# These functions retrieve component items from a ship

async def get_ship_weapon(ship_id: int) -> Optional[Dict]:
    """Get a ship's weapon component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Weapon item dict, or None if no weapon equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        weapon_id = ship.get('weapon_id')
        
        if weapon_id is None or not isinstance(weapon_id, int):
            return None
        
        return await dh.get_item(weapon_id)
    except KeyError:
        return None


async def get_ship_shield(ship_id: int) -> Optional[Dict]:
    """Get a ship's shield component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Shield item dict, or None if no shield equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        shield_id = ship.get('shield_id')
        
        if shield_id is None or not isinstance(shield_id, int):
            return None
        
        return await dh.get_item(shield_id)
    except KeyError:
        return None


async def get_ship_engine(ship_id: int) -> Optional[Dict]:
    """Get a ship's engine component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Engine item dict, or None if no engine equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        engine_id = ship.get('engine_id')
        
        if engine_id is None or not isinstance(engine_id, int):
            return None
        
        return await dh.get_item(engine_id)
    except KeyError:
        return None


async def get_ship_cargo(ship_id: int) -> Optional[Dict]:
    """Get a ship's cargo component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Cargo item dict, or None if no cargo equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        cargo_id = ship.get('cargo_id')
        
        if cargo_id is None or not isinstance(cargo_id, int):
            return None
        
        return await dh.get_item(cargo_id)
    except KeyError:
        return None


async def get_ship_sensor(ship_id: int) -> Optional[Dict]:
    """Get a ship's sensor component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Sensor item dict, or None if no sensor equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        sensor_id = ship.get('sensor_id')
        
        if sensor_id is None or not isinstance(sensor_id, int):
            return None
        
        return await dh.get_item(sensor_id)
    except KeyError:
        return None


async def get_ship_stealth_cloak(ship_id: int) -> Optional[Dict]:
    """Get a ship's stealth cloak component.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Stealth cloak item dict, or None if no stealth cloak equipped
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        stealth_id = ship.get('stealth_cloak_id')
        
        if stealth_id is None or not isinstance(stealth_id, int):
            return None
        
        return await dh.get_item(stealth_id)
    except KeyError:
        return None


# ============================================================================
# STAT CALCULATIONS
# ============================================================================
# These functions calculate ship stats based on tier and component multipliers

async def get_ship_max_hp(ship_id: int) -> float:
    """Calculate a ship's maximum HP based on its tier.
    
    Formula: 100 * ((1 + tier) ^ 2)
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Maximum HP as a float
    """
    dh = _get_data_handler()
    ship = await dh.get_ship(ship_id)
    tier = ship['tier']
    return 100.0 * math.pow(1 + tier, 2)


async def get_ship_weapon_damage(ship_id: int) -> float:
    """Calculate a ship's weapon damage.
    
    Returns the weapon's multiplier if health > 0, or 0 if no weapon equipped or weapon disabled.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Damage value as a float
    """
    weapon = await get_ship_weapon(ship_id)
    if weapon is None:
        return 0.0
    
    # Check if weapon is disabled (health <= 0)
    health = weapon['health']
    if health <= 0:
        return 0.0
    
    return float(weapon['multiplier'])


async def get_ship_cargo_capacity(ship_id: int) -> float:
    """Calculate a ship's cargo capacity.
    
    Formula: 100 * (1 + cargo_tier) * cargo_multiplier
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Cargo capacity as a float
    """
    cargo = await get_ship_cargo(ship_id)
    if cargo is None:
        return 0.0
    
    tier = cargo['tier']
    multiplier = cargo['multiplier']
    
    return 100.0 * (1 + tier) * multiplier


async def get_ship_max_shield_pool(ship_id: int) -> float:
    """Calculate a ship's maximum shield pool capacity.
    
    Formula: 50 * ((1 + shield_tier) ^ 1.5) * shield_multiplier
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Maximum shield pool as a float, or 0 if no shield equipped
    """
    shield = await get_ship_shield(ship_id)
    if shield is None:
        return 0.0
    
    tier = shield['tier']
    multiplier = shield['multiplier']
    
    return 50.0 * math.pow(1 + tier, 1.5) * multiplier


async def get_ship_current_shield_pool(ship_id: int) -> float:
    """Get a ship's current shield pool value.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Current shield pool as a float
    """
    dh = _get_data_handler()
    ship = await dh.get_ship(ship_id)
    return float(ship['shield_pool'])


# ============================================================================
# DAMAGE AND REPAIR FUNCTIONS
# ============================================================================

async def repair_ship_hp(ship_id: int) -> float:
    """Fully repair a ship's HP to maximum (thread-safe).
    
    Ship HP repairs are simple - no penalties or multiplier changes.
    
    Args:
        ship_id: Ship ID to repair
        
    Returns:
        Amount of HP restored
        
    Raises:
        KeyError: If ship doesn't exist
    """
    dh = _get_data_handler()
    ship = await dh.get_ship(ship_id)
    
    # Get current HP before repair
    current_hp = ship['hp']
    
    # Calculate max HP
    max_hp = await get_ship_max_hp(ship_id)
    
    # Use DataHandler's set_ship_to_max_hp method
    await dh.set_ship_to_max_hp(ship_id)
    
    # Return amount restored
    return max_hp - current_hp


async def refill_shield_pool(ship_id: int) -> float:
    """Refill a ship's shield pool to maximum (thread-safe).
    
    Shield pool refills are simple - like refilling a tank of gas at a starport.
    
    Args:
        ship_id: Ship ID to refill shields
        
    Returns:
        Amount of shield pool restored
        
    Raises:
        KeyError: If ship doesn't exist
    """
    dh = _get_data_handler()
    ship = await dh.get_ship(ship_id)
    
    # Get current shield pool before refill
    current_shield = ship['shield_pool']
    
    # Calculate max shield pool
    max_shield = get_ship_max_shield_pool(ship_id)
    
    # Use DataHandler's set_shield_to_max method
    await dh.set_shield_to_max(ship_id)
    
    # Return amount restored
    return max_shield - current_shield


async def _calculate_multiplier_reduction(health_percent: float) -> float:
    """Calculate the multiplier reduction based on remaining health percentage.
    
    Health %      -> Multiplier Reduction
    0-9%          -> 0.10
    10-19%        -> 0.09
    20-29%        -> 0.08
    30-39%        -> 0.07
    40-49%        -> 0.06
    50-59%        -> 0.05
    60-69%        -> 0.04
    70-79%        -> 0.03
    80-89%        -> 0.02
    90-99%        -> 0.01
    100%          -> 0.00
    
    Args:
        health_percent: Health percentage (0.0 to 100.0)
        
    Returns:
        Multiplier reduction as a float
    """
    if health_percent >= 100.0:
        return 0.0
    elif health_percent >= 90.0:
        return 0.01
    elif health_percent >= 80.0:
        return 0.02
    elif health_percent >= 70.0:
        return 0.03
    elif health_percent >= 60.0:
        return 0.04
    elif health_percent >= 50.0:
        return 0.05
    elif health_percent >= 40.0:
        return 0.06
    elif health_percent >= 30.0:
        return 0.07
    elif health_percent >= 20.0:
        return 0.08
    elif health_percent >= 10.0:
        return 0.09
    else:  # 0-9%
        return 0.10


async def repair_component(item_id: int) -> Dict[str, float]:
    """Repair a component by restoring its health to max and applying multiplier reduction.
    
    The component's health is restored to maximum, but the multiplier is reduced based
    on the health percentage at the time of repair. This creates a permanent penalty
    for letting components get too damaged.
    
    Multiplier reduction is calculated based on health % before repair:
    - 0-9% health: -0.10 multiplier
    - 10-19% health: -0.09 multiplier
    - 20-29% health: -0.08 multiplier
    - ... up to ...
    - 90-99% health: -0.01 multiplier
    - 100% health: no reduction
    
    Args:
        item_id: ID of the component item to repair
        
    Returns:
        Dict with repair info: {
            'health_restored': float,
            'multiplier_reduction': float,
            'new_multiplier': float,
            'health_percent_before': float
        }
        
    Raises:
        KeyError: If item doesn't exist
        ValueError: If item is not a component type
    """
    dh = _get_data_handler()
    component = await dh.get_item(item_id)
    
    # Verify this is a component
    item_type = component['type']
    valid_types = ['engine', 'weapon', 'shield', 'cargo', 'sensor', 'stealth_cloak']
    if item_type not in valid_types:
        raise ValueError(f"Item {item_id} is not a component (type: '{item_type}'). Must be one of {valid_types}")
    
    # Get current values
    current_health = component['health']
    current_mult = component['multiplier']
    min_mult = component['min_multiplier']
    
    # Get max health from the item's maxhealth field
    max_health = component['maxhealth']
    
    # Calculate health percentage
    health_percent = (current_health / max_health * 100.0) if max_health > 0 else 100.0
    
    # Calculate multiplier reduction based on health %
    multiplier_reduction = _calculate_multiplier_reduction(health_percent)
    
    # Calculate new multiplier (can't go below min_multiplier)
    new_multiplier = max(min_mult, current_mult - multiplier_reduction)
    
    # Calculate health restored
    health_restored = max_health - current_health
    
    # Apply repairs using DataHandler's methods
    await dh.set_item_to_max_health(item_id)
    await dh.update_item_multiplier(item_id, new_multiplier)
    
    return {
        'health_restored': health_restored,
        'multiplier_reduction': multiplier_reduction,
        'new_multiplier': new_multiplier,
        'health_percent_before': health_percent
    }




# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def can_equip_item(ship_id: int, item_id: int) -> bool:
    """Check if a ship can equip an item based on tier restrictions.
    
    A ship can only equip items with tier <= ship tier + 2.
    
    Args:
        ship_id: Ship ID
        item_id: Item ID to check
        
    Returns:
        True if ship can equip the item, False otherwise
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        item = await dh.get_item(item_id)
        
        ship_tier = ship['tier']
        item_tier = item['tier']
        
        return item_tier <= ship_tier + 2
    except KeyError:
        return False


async def get_ship_total_cargo_weight(ship_id: int) -> float:
    """Calculate the total weight of items in a ship's cargo.
    
    Args:
        ship_id: Ship ID
        
    Returns:
        Total cargo weight as a float
    """
    dh = _get_data_handler()
    try:
        ship = await dh.get_ship(ship_id)
        item_ids = ship['items']
        
        total_weight = 0.0
        for item_id in item_ids:
            try:
                item = await dh.get_item(item_id)
                total_weight += item['weight']
            except KeyError:
                continue  # Skip missing items
        
        return total_weight
    except KeyError:
        return 0.0


async def can_fit_item_in_cargo(ship_id: int, item_id: int) -> bool:
    """Check if an item can fit in a ship's cargo based on weight.
    
    Args:
        ship_id: Ship ID
        item_id: Item ID to check
        
    Returns:
        True if item fits, False otherwise
    """
    dh = _get_data_handler()
    try:
        item = await dh.get_item(item_id)
        item_weight = item['weight']
        
        current_weight = get_ship_total_cargo_weight(ship_id)
        capacity = get_ship_cargo_capacity(ship_id)
        
        return (current_weight + item_weight) <= capacity
    except KeyError:
        return False


__all__ = [
    # Component getters
    'get_ship_weapon',
    'get_ship_shield',
    'get_ship_engine',
    'get_ship_cargo',
    'get_ship_sensor',
    'get_ship_stealth_cloak',
    
    # Stat calculations
    'get_ship_max_hp',
    'get_ship_weapon_damage',
    'get_ship_cargo_capacity',
    'get_ship_max_shield_pool',
    'get_ship_current_shield_pool',
    
    # Repair functions
    'repair_ship_hp',
    'refill_shield_pool',
    'repair_component',
    
    # Utilities
    'can_equip_item',
    'get_ship_total_cargo_weight',
    'can_fit_item_in_cargo',
]
