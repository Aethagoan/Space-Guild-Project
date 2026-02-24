# Aidan Orion 23 Feb 2026

# Item Dictionary Creator.


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


# an implementation note - Items aren't given a location key because it is far faster to return things given a list of their IDs, instead of iterating the whole item list (millions of items) just to get ten back.

def Item(ID:int,name:str,tier:int,health:int,weight:float,mult:float,item_type:str):
    return {
        'id': ID,
        'name': name,
        'tier': tier,
        'type': item_type,
        'health': health,
        'weight': weight,
        'multiplier': mult,
        'min_multiplier': get_min_multiplier(tier),
        'max_multiplier': get_max_multiplier(tier),
    }

# Dropped Generated Items Are Likely to have a random mult, items players buy/quest for are likely to start at the max mult.

def Engine(ID_:int,name_:str,tier_:int,mult_:float):

    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=40*(1+tier_), 
        weight=40*(1+tier_), 
        mult=mult_,
        item_type='engine',
    )


def Weapon(ID_:int,name_:str,tier_:int,mult_:float):
    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=50*(1+tier_), 
        weight=10*(1+tier_), 
        mult=mult_,
        item_type='weapon',
    )


def Sensor(ID_:int,name_:str,tier_:int,mult_:float):
    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=25*(1+tier_), 
        weight=20*(1+tier_), 
        mult=mult_,
        item_type='sensor',
    )

def Cargo(ID_:int,name_:str,tier_:int,mult_:float):
    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=100*(1+tier_), 
        weight=40*(1+tier_), 
        mult=mult_,
        item_type='cargo',
    )


def Shield(ID_:int,name_:str,tier_:int,mult_:float):
    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=25*(1+tier_), 
        weight=40*(1+tier_), 
        mult=mult_,
        item_type='shield',
    )

def StealthCloak(ID_:int,name_:str,tier_:int,mult_:float):
    return Item(
        ID=ID_,
        name=name_,
        tier=tier_, 
        health=40*(1+tier_), 
        weight=20*(1+tier_), 
        mult=mult_,
        item_type='stealth_cloak',
    )