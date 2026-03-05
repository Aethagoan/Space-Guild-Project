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


base_weapon_damage = 25


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
    
    Returns the weapon's multiplier*base_weapon_damage if health > 0, or 0 if no weapon equipped or weapon disabled.
    
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
    
    return float(weapon['multiplier'] * base_weapon_damage * (weapon['tier'] + 1))


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
    
    # Utilities
    'can_equip_item',
    'get_ship_total_cargo_weight',
    'can_fit_item_in_cargo',
]
