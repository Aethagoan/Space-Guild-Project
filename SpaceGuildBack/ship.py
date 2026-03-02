# Aidan Orion 23 Feb 2026

# stats, carrying capacity, stuff like that should be kept track of in another dictionary for quick lookup (all based on tier and multiplier.)

from typing import Optional

def get_ship_tier_hp(tier: int) -> float:
    """Calculate the maximum HP for a ship based on its tier.
    
    Formula: 100 * ((1 + tier) ^ 2)
    
    Args:
        tier: Ship tier (0-6)
        
    Returns:
        Maximum HP for the given tier
        
    Examples:
        tier 0: 100.0 HP
        tier 1: 400.0 HP
        tier 2: 900.0 HP
        tier 3: 1600.0 HP
        tier 4: 2500.0 HP
        tier 5: 3600.0 HP
        tier 6: 4900.0 HP
    """
    return 100.0 * ((1 + tier) ** 2)

def Ship(location: Optional[str] = None):
    return {
        'hp': 100.0,  # Current HP (float)
        'tier': 0,
        'location': location,  # Current location name (synced with location's ship_ids list)
        'shield_pool': 0.0,  # Current shield pool (float)
        # all of these are considered Items.
        'engine_id': None,
        'weapon_id': None,
        'shield_id': None,
        'cargo_id': None,
        'sensor_id': None,
        'stealth_cloak_id': None,
        'items': [],
    }



