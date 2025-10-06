import unittest
import SpaceGuildBack.spaceshipComponent as spc
import SpaceGuildBack.location as loc

class TestCargo(unittest.TestCase):
    def test_init(self):
        cargo = spc.Cargo('basic cargo', 0)
        self.assertIsNotNone(cargo)
        self.assertIn('items', cargo)
        self.assertIsInstance(cargo['items'], list)

    def test_add_item(self):
        cargo = spc.Cargo('basic cargo', 0)
        result = spc.add_item(cargo, "Item1", 10)
        self.assertTrue(result)
        self.assertEqual(len(cargo['items']), 1)
    # LLM-Dev: v1 - verify capacity logic via helper
        self.assertTrue(spc.can_fit_item(cargo, cargo['capacity'] - spc.total_cargo_weight(cargo)))

    def test_take_damage(self):
        cargo = spc.Cargo('basic cargo', 0)
        spc.apply_damage(cargo, 5)
        self.assertEqual(cargo['health'], 95)

class TestLocationThings(unittest.TestCase):
	def locationsarecreatedcorrectly(self):
		loc.addnewlocation('earth')
		self.assertTrue(len(loc.locationhandler.keys()) == 1)
		loc.locationhandler.clear()
    
	def locationslinkcorrectly(self):
      
		loc.addnewlocation('earth')
		loc.addnewlocation('mars')
		loc.addnewlocation('jupiter')
            
		loc.linklocations('earth','mars')
		loc.linklocations('mars','jupiter')
      
		self.assertTrue(loc.locationhandler['earth'].links.__contains__('mars'))
		self.assertTrue(loc.locationhandler['mars'].links.__contains__('earth'))
		self.assertFalse(loc.locationhandler['earth'].links__contains__('jupiter'))

		loc.locationhandler.clear()



if __name__ == '__main__':
    unittest.main()
