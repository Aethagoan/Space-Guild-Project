from classes import *

class Ship:
    def __init__(self):
        self.health = 0
        self.engine = Engine()
        self.weapon = Weapon()
        self.shield = Shield()
        self.cargo = Cargo()
        self.sensor = Sensor()
        self.stealth_cloak = StealthCloak()
