"""Automatic unittesting"""
import unittest

import state

from modules import ModuleBase
from modules.log import Log

from shadowui import Section

class AutoTesterModule(ModuleBase):
    """Program integrity testing suite"""
    name = "autotester"
    short = "test"
    def load(self):
        pass

    def unload(self):
        pass

    def run(self, **kwargs):
        log = Log("Autotester")
        log.info("Finding tests...")
        testsuite = unittest.TestLoader().discover('.')
        log.info("Running tests...")
        unittest.TextTestRunner(verbosity=1).run(testsuite)
        log.info("Tests done.")
        del log
        raise state.ProgramExit()

        
#register to main program as a module
state.modules.append(AutoTesterModule())