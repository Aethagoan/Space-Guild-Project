


def whatismaxmultiplier(Tier:ComponentTier):
    if (Tier is ComponentTier0):
        return 1
    elif (Tier is ComponentTier1):
        return 2
    elif (Tier is ComponentTier2):
        return 3
    elif (Tier is ComponentTier3):
        return 4
    elif (Tier is ComponentTier4):
        return 6
    elif (Tier is ComponentTier5):
        return 8
    elif (Tier is ComponentTier6):
        return 10

 
# base class for connectivity
class ComponentTier:
    @abstractmethod
    def __init__(self):
        pass

# all of the tiers that are considered the same class
class ComponentTier0(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 1

class ComponentTier1(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 1

class ComponentTier2(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 2

class ComponentTier3(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 3

class ComponentTier4(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 4

class ComponentTier5(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 6

class ComponentTier6(ComponentTier):
    def __init__(self):
        self.min_tier_multiplier = 8


class ShipComponent:
    def __init__(self, name: str, multiplier: float, tier: ComponentTier):
        self.tier = tier
        self.name = name
        self.health = 100
        self.min_tier_multiplier = tier.min_tier_multiplier
        self.multiplier = multiplier

    def repair(self, amount: int):
        self.health = max_health
        if self.mulitplier < tier.min_tier_multiplier:
            self.multiplier = self.min_tier_multiplier
    
    def damage(self, damage:int):
        remaining = self.health - damage
        if remaining < 0:
            self.health = 0
            pass # death 

        elif self.health > self.max_health * .75 > remaining:
            self.multiplier -= .1

        elif self.health > self.max_health * .5 > remaining:
            self.multiplier -= .1

        elif self.health > self.max_health * .25 > remaining:
            self.multiplier -= .1

        self.health = remaining



class Engine(ShipComponent):
    def __init__(self, Tier:ComponentTier):
        super().__init__("Engine/Warp Drive/Propulsion", 100, 1.0, Tier)

    @property
    def max_health(self) -> int:
        return 100 * whatismaxmultiplier(Tier)


class Weapon(ShipComponent):
    def __init__(self, Tier:ComponentTier):
        super().__init__("Weapons", 50, 1.0, Tier)

    @property
    def max_health(self) -> int:
        return 50 * whatismaxmultiplier(Tier)


class Shield(ShipComponent):
    def __init__(self, Tier:ComponentTier):
        super().__init__("Shields", 200, 1.0, Tier)
        self.shield_pool = 200 * whatismaxmultiplier(Tier)

    @property
    def max_health(self) -> int:
        return 25 * whatismaxmultiplier(Tier)

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
    def __init__(self, Tier:ComponentTier):
        super().__init__("Cargo", 100, 1.0, Tier)
        self.capacity = 100
        self.items = []

    @property
    def max_health(self) -> int:
        return 100 * whatismaxmultiplier(Tier)

    def add_item(self, name: str, size: int) -> bool:
        if self.capacity - size >= 0:
            self.items.append(CargoItem(name, size))
            self.capacity -= size
            return True
        return False


class Sensor(ShipComponent):
    def __init__(self, Tier:ComponentTier):
        super().__init__("Sensors", 30, 1.0, Tier)
        self.scan_range = 5
        self.detail_level = 0.8

    @property
    def max_health(self) -> int:
        return 30 * whatismaxmultiplier(Tier)


class StealthCloak(ShipComponent):
    def __init__(self, Tier:ComponentTier):
        super().__init__("Stealth Cloak", 20, 1.0, Tier)
        self.stealth_active = False

    @property
    def max_health(self) -> int:
        return 20 * whatismaxmultiplier(Tier)

    def activate(self):
        self.stealth_active = True

    def deactivate(self):
        self.stealth_active = False