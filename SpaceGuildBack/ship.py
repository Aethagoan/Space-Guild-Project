# Aidan Orion 23 Feb 2026

# stats, carrying capacity, stuff like that should be kept track of in another dictionary for quick lookup (all based on tier and multiplier.)

def Ship(location: str = None):
    return {
        'hp': 100.0,  # Current HP (float)
        'tier': 0,
        'location': location,  # Current location name (synced with location's ship_ids list)
        'shield_pool': 0.0,  # Current shield pool (float)
        # all of these are considered Items.
        'engine_id': int,
        'weapon_id': int,
        'shield_id': int,
        'cargo_id': int,
        'sensor': int,
        'stealth_cloak_id': int,
        'items': [],
    }


