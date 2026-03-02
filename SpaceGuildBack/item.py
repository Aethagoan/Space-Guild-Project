# Aidan Orion 23 Feb 2026

# Item Dictionary Creator.

import datetime
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from data import DataHandler

# Import will happen at runtime to avoid circular imports
data_handler = None

def _get_data_handler():
    """Lazy import to avoid circular dependency."""
    global data_handler
    if data_handler is None:
        from program import data_handler as dh
        data_handler = dh
    return data_handler

# weapon damage is based off of these numbers. I want a weapon to kill most components in around two hits at the same tier,
# therefore a t0 weapon should be doing about 20 damage.
# the shield pool should take something like 4 of these hits, so the base should be 80.
engine_base_health = 50.0
weapon_base_health = 25.0
shield_base_health = 25.0
cargo_base_health = 100.0
sensor_base_health = 25.0
stealth_cloak_base_health = 40.0

# this is for capacity reasons, t0 base cargo capacity is 100.
# the implication is that it's hard to carry things that are higher teir without upgrading the ship's cargo item first.
engine_base_weight = 40.0
weapon_base_weight = 10.0
shield_base_weight = 40.0
cargo_base_weight = 40.0
sensor_base_weight = 20.0
stealth_cloak_base_weight = 20.0

def get_max_multiplier(tier: int):
    maxmultipliers = [1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0]
    if 0 <= tier < len(maxmultipliers):
        return maxmultipliers[tier]
    raise ValueError("Invalid tier")

def get_min_multiplier(tier: int):
    minmultipliers = [0.5, 0.8, 1.5, 2.0, 3.0, 5.0, 6.0]
    if 0 <= tier < len(minmultipliers):
        return minmultipliers[tier]
    raise ValueError("Invalid tier")


# ============================================================================
# ITEM DAMAGE/HEAL/REPAIR FUNCTIONS
# ============================================================================

def _calculate_component_multiplier_reduction(health_percent: float) -> float:
    """Calculate multiplier reduction for COMPONENTS based on health percentage.
    
    Components have lenient degradation penalties.
    
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


def _calculate_item_multiplier_reduction(health_percent: float) -> float:
    """Calculate multiplier reduction for ITEMS (non-components) based on health percentage.
    
    Items have SEVERE degradation penalties - more harsh than components.
    
    Health %      -> Multiplier Reduction
    0-9%          -> 0.50
    10-19%        -> 0.45
    20-29%        -> 0.40
    30-39%        -> 0.35
    40-49%        -> 0.30
    50-59%        -> 0.25
    60-69%        -> 0.20
    70-79%        -> 0.15
    80-89%        -> 0.10
    90-99%        -> 0.05
    100%          -> 0.00
    
    Args:
        health_percent: Health percentage (0.0 to 100.0)
        
    Returns:
        Multiplier reduction as a float
    """
    if health_percent >= 100.0:
        return 0.0
    elif health_percent >= 90.0:
        return 0.05
    elif health_percent >= 80.0:
        return 0.10
    elif health_percent >= 70.0:
        return 0.15
    elif health_percent >= 60.0:
        return 0.20
    elif health_percent >= 50.0:
        return 0.25
    elif health_percent >= 40.0:
        return 0.30
    elif health_percent >= 30.0:
        return 0.35
    elif health_percent >= 20.0:
        return 0.40
    elif health_percent >= 10.0:
        return 0.45
    else:  # 0-9%
        return 0.50


def damage_item(item_id: int, damage: float) -> Dict[str, Any]:
    """Apply damage to an item's health (thread-safe via DataHandler).
    
    This is a convenience wrapper around DataHandler.damage_item() that provides
    the same functionality but can be called from item.py context.
    
    Args:
        item_id: Item ID to damage
        damage: Amount of damage to apply (must be positive)
        
    Returns:
        Dict with damage results: {
            'health_damage': float,
            'remaining_health': float,
            'disabled': bool
        }
        
    Raises:
        KeyError: If item doesn't exist
        ValueError: If damage is negative
    """
    if damage < 0:
        raise ValueError(f"damage must be positive, got {damage}")
    
    dh = _get_data_handler()
    return dh.damage_item(item_id, damage)


def heal_item(item_id: int, heal_amount: float) -> float:
    """Heal an item's health without any penalties (thread-safe via DataHandler).
    
    This is simple healing - no multiplier reduction. Health is clamped to maxhealth.
    
    Args:
        item_id: Item ID to heal
        heal_amount: Amount of health to restore (must be positive)
        
    Returns:
        Actual amount of health restored (capped by maxhealth)
        
    Raises:
        KeyError: If item doesn't exist
        ValueError: If heal_amount is negative
    """
    if heal_amount < 0:
        raise ValueError(f"heal_amount must be positive, got {heal_amount}")
    
    dh = _get_data_handler()
    dh.heal_item_health(item_id, heal_amount)
    
    # Calculate actual amount healed
    item = dh.get_item(item_id)
    current_health = item['health']
    max_health = item['maxhealth']
    
    # Return the amount actually healed (min of heal_amount and room left)
    return min(heal_amount, max_health - current_health + heal_amount)


def repair_item(item_id: int) -> Dict[str, float]:
    """Repair an item by restoring health to max and applying multiplier reduction.
    
    Items (non-components) have SEVERE degradation penalties compared to components.
    This reflects that items are more fragile and less maintainable.
    
    Multiplier reduction for items (harsh):
    - 0-9% health: -0.50 multiplier
    - 10-19% health: -0.45 multiplier
    - 20-29% health: -0.40 multiplier
    - 30-39% health: -0.35 multiplier
    - 40-49% health: -0.30 multiplier
    - 50-59% health: -0.25 multiplier
    - 60-69% health: -0.20 multiplier
    - 70-79% health: -0.15 multiplier
    - 80-89% health: -0.10 multiplier
    - 90-99% health: -0.05 multiplier
    - 100% health: no reduction
    
    Args:
        item_id: ID of the item to repair
        
    Returns:
        Dict with repair info: {
            'health_restored': float,
            'multiplier_reduction': float,
            'new_multiplier': float,
            'health_percent_before': float
        }
        
    Raises:
        KeyError: If item doesn't exist
    """
    dh = _get_data_handler()
    item = dh.get_item(item_id)
    
    # Get current values
    current_health = item['health']
    max_health = item['maxhealth']
    current_mult = item['multiplier']
    min_mult = item['min_multiplier']
    item_type = item['type']
    
    # Calculate health percentage
    health_percent = (current_health / max_health * 100.0) if max_health > 0 else 100.0
    
    # Determine if this is a component or regular item
    component_types = ['engine', 'weapon', 'shield', 'cargo', 'sensor', 'stealth_cloak']
    is_component = item_type in component_types
    
    # Calculate multiplier reduction based on item type
    if is_component:
        multiplier_reduction = _calculate_component_multiplier_reduction(health_percent)
    else:
        multiplier_reduction = _calculate_item_multiplier_reduction(health_percent)
    
    # Calculate new multiplier (can't go below min_multiplier)
    new_multiplier = max(min_mult, current_mult - multiplier_reduction)
    
    # Calculate health restored
    health_restored = max_health - current_health
    
    # Apply repairs using DataHandler's methods
    dh.set_item_to_max_health(item_id)
    dh.update_item_multiplier(item_id, new_multiplier)
    
    return {
        'health_restored': health_restored,
        'multiplier_reduction': multiplier_reduction,
        'new_multiplier': new_multiplier,
        'health_percent_before': health_percent
    }


def set_item_health(item_id: int, health: float):
    """Set an item's health directly (thread-safe via DataHandler).
    
    ⚠️ WARNING: FOR TESTING ONLY! ⚠️
    This method bypasses normal game mechanics and should ONLY be used in tests.
    In production code, use damage_item() or heal_item() instead.
    
    Args:
        item_id: Item ID
        health: New health value
        
    Raises:
        KeyError: If item doesn't exist
    """
    dh = _get_data_handler()
    dh.set_item_health(item_id, health)


# ============================================================================
# ITEM CREATION FUNCTIONS
# ============================================================================

# an implementation note - Items aren't given a location key because it is far faster to return things given a list of their IDs, instead of iterating the whole item list (millions of items) just to get ten back.

def Item(ID:int,name:str,tier:int,maxhealth:float,health:float,weight:float,mult:float,item_type:str,description:str=""):
    return {
        'id': ID,
        'name': name,
        'description':description,
        'tier': tier,
        'type': item_type,
        'maxhealth':maxhealth,
        'health': health,
        'weight': weight,
        'multiplier': mult,
        'min_multiplier': get_min_multiplier(tier),
        'max_multiplier': get_max_multiplier(tier),
        'created_at': datetime.datetime.now().timestamp(), # no need to convert back, this should be a float and just comparable by itself.
    }


# Dropped Generated Items Are Likely to have a random mult, items players buy/quest for are likely to start at the max mult.

def Engine(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(engine_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health,
        health=calc_max_health,
        weight=float(engine_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='engine',
    )

def Weapon(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(weapon_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health, 
        health=calc_max_health, 
        weight=float(weapon_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='weapon',
    )

def Sensor(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(sensor_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health,
        health=calc_max_health,
        weight=float(sensor_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='sensor',
    )

def Cargo(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(cargo_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health, 
        health=calc_max_health, 
        weight=float(cargo_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='cargo',
    )


def Shield(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(shield_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health, 
        health=calc_max_health, 
        weight=float(shield_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='shield',
    )

def StealthCloak(ID_:int,name_:str,tier_:int,mult_:float,description_:str=""):

    calc_max_health = float(stealth_cloak_base_health*(1+tier_))

    return Item(
        ID=ID_,
        name=name_,
        description=description_,
        tier=tier_, 
        maxhealth=calc_max_health, 
        health=calc_max_health, 
        weight=float(stealth_cloak_base_weight*(1+tier_)), 
        mult=mult_,
        item_type='stealth_cloak',
    )
