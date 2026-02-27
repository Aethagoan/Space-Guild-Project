# Aidan Orion 23 Feb 2026

# Item Dictionary Creator.

import datetime

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