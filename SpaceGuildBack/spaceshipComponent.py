

def get_max_multiplier(tier: int):
    maxmultipliers = [1, 2, 3, 4, 6, 8, 10]
    if 0 <= tier < len(maxmultipliers):
        return maxmultipliers[tier]
    raise ValueError("Invalid tier")

def get_min_multiplier(tier: int):
    minmultipliers = [1, 1, 2, 3, 4, 6, 8]
    if 0 <= tier < len(minmultipliers):
        return minmultipliers[tier]
    raise ValueError("Invalid tier")

def Engine(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 100 * (1 + tier),
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }

def Weapon(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 50 * (1 + tier),
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }

def Cargo(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 100 * (1 + tier),
        'capacity': 100 * (1+tier),
        'items': [],
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }

def Sensor(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 25 * (1 + tier),
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }

def Shield(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 25 * (1 + tier),
        'pool': 200 * (1 + tier),
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }

def StealthCloak(name:str,tier:int):
    return {
        'name': name,
        'tier': tier,
        'health': 25 * (1 + tier),
        'multiplier': get_max_multiplier(tier),
        'maxmultiplier': get_max_multiplier(tier),
        'minmultiplier': get_min_multiplier(tier)
    }



def total_cargo_weight(cargo: dict) -> int:
    """Sum weights of items stored as {'name': str, 'weight': int} dicts."""
    return sum(item.get('weight', 0) for item in cargo.get('items', []))


def can_fit_item(cargo: dict, weight: int) -> bool:
    """Return True if the item of a given weight fits within remaining capacity."""
    # Capacity defined by cargo['capacity']; items tracked in cargo['items'].
    return (total_cargo_weight(cargo) + weight) <= cargo.get('capacity', 0)


def add_item(cargo: dict, name: str, weight: int) -> bool:
    """Attempt to add an item; returns True if added, False otherwise."""
    if can_fit_item(cargo, weight):
        cargo.setdefault('items', []).append({'name': name, 'weight': weight})
        return True
    return False


def apply_damage(component: dict, amount: int) -> None:
    """Reduce a component's 'health' without going below zero."""
    component['health'] = max(0, component.get('health', 0) - amount)
