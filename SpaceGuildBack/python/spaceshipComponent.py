from classes import *


class ComponentTier:
    Tier0 = 0
    Tier1 = 1
    Tier2 = 2
    Tier3 = 3
    Tier4 = 4
    Tier5 = 5
    Tier6 = 6


class ShipComponent:
    def __init__(self, name: str, health: int, damage_multiplier: float, tier: ComponentTier):
        self.name = name
        self.health = health
        self.damage_multiplier = damage_multiplier
        self.tier = tier

    def repair(self, amount: int):
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount


class Engine(ShipComponent):
    def __init__(self):
        super().__init__("Engine/Warp Drive/Propulsion", 100, 1.0, ComponentTier.Tier0)

    @property
    def max_health(self) -> int:
        return 100


class Weapon(ShipComponent):
    def __init__(self):
        super().__init__("Weapons", 50, 1.0, ComponentTier.Tier0)

    @property
    def max_health(self) -> int:
        return 50


class Shield(ShipComponent):
    def __init__(self):
        super().__init__("Shields", 200, 1.0, ComponentTier.Tier0)
        self.shield_pool = self.health

    @property
    def max_health(self) -> int:
        return 200

    def take_damage(self, amount: int):
        if self.shield_pool > 0:
            self.shield_pool -= amount
        else:
            self.health -= amount


class CargoItem:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Cargo(ShipComponent):
    def __init__(self):
        super().__init__("Cargo", 100, 1.0, ComponentTier.Tier0)
        self.capacity = 100
        self.items = []

    @property
    def max_health(self) -> int:
        return 100

    def add_item(self, name: str, size: int) -> bool:
        if self.capacity - size >= 0:
            self.items.append(CargoItem(name, size))
            self.capacity -= size
            return True
        return False


class Sensor(ShipComponent):
    def __init__(self):
        super().__init__("Sensors", 30, 1.0, ComponentTier.Tier0)
        self.scan_range = 5
        self.detail_level = 0.8

    @property
    def max_health(self) -> int:
        return 30


class StealthCloak(ShipComponent):
    def __init__(self):
        super().__init__("Stealth Cloak", 20, 1.0, ComponentTier.Tier0)
        self.active = False

    @property
    def max_health(self) -> int:
        return 20

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False