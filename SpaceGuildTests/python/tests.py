import unittest
from SpaceGuildBack.python.spaceshipComponent import *
from SpaceGuildBack.python.location import *
from SpaceGuildBack.python.spaceship import *

class TestCargo(unittest.TestCase):
    def test_init(self):
        cargo = Cargo()
        self.assertIsNotNone(cargo)

    def test_add_item(self):
        cargo = Cargo()
        result = cargo.add_item("Item1", 10)
        self.assertTrue(result)
        self.assertEqual(len(cargo.items), 1)

    def test_take_damage(self):
        cargo = Cargo()
        cargo.damage(5)
        self.assertEqual(cargo.health, 95)

class TestLocationThings(unittest.TestCase):
    def location_movment(self):
        loc1 = Orbit()



if __name__ == '__main__':
    unittest.main()
