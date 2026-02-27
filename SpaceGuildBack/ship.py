# Aidan Orion 23 Feb 2026

# stats, carrying capacity, stuff like that should be kept track of in another dictionary for quick lookup (all based on tier and multiplier.)

def Ship(location: str = None):
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


