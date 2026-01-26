from spaceshipComponent import *

def Ship(location:str):
    return {
        'hp': 100,
        'location': location,
        'engine': Engine('basic engine',0),
        'weapon': Weapon('basic gun',0),
        'shield': Shield('basic shield',0),
        'cargo': Cargo('basic cargo',0),
        'sensor': Sensor('basic sensor',0),
        'stealth_cloak': None
    }
