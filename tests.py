import unittest
from main import *
import math

class TestCaseGames(unittest.TestCase):

    def test_singleton(self):
        config_manager = ConfigManager()
        config_manager.set_param_value("Name", "Testcase")
        config = ConfigManager()
        
        self.assertEqual(config_manager.get_param_value("Name"), config.get_param_value("Name"))
    
    def test_distance(self):
        self.assertEqual(distance((0,0), (0,0)), 0.7071067811865476)
        self.assertEqual(distance((0.5,0.5), (0,0)), math.sqrt(2))
        #self.assertTrue()
        #self.assertFalse()
    

unittest.main()