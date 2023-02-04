
import unittest

from modules.modulebase import ModuleBase, ModuleAlreadyLoaded, ModuleAlreadyUnLoaded
from modules.log import Log

class TestModuleBase(unittest.TestCase):
    def setUp(self):
        self.modbase = ModuleBase()
        self.modlog = ModuleBase()

    def tearDown(self):
        del self.modbase
        del self.modlog

    def test_log_exceptions(self):
        self.modbase.load()
        self.modlog.load()
    
        #try double loading
        self.assertRaises(ModuleAlreadyLoaded, self.modbase.load)
        self.assertRaises(ModuleAlreadyLoaded, self.modlog.load)
        
        self.modlog.unload()
        self.modbase.unload()
        #try double unloading
        self.assertRaises(ModuleAlreadyUnLoaded, self.modbase.unload)
        self.assertRaises(ModuleAlreadyUnLoaded, self.modlog.unload)