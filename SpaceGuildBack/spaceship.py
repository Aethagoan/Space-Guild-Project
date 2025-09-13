import spaceshipComponent

class Ship:
    def __init__(self):
        self.health = 100
        self.engine = spaceshipComponent.Engine()
        self.weapon = spaceshipComponent.Weapon()
        self.shield = spaceshipComponent.Shield()
        self.cargo = spaceshipComponent.Cargo()
        self.sensor = spaceshipComponent.Sensor()
        self.stealth_cloak = spaceshipComponent.StealthCloak()
