

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


