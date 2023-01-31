"""Automatic unittesting"""
import unittest

import state

from modules.log import Log

from shadowui import Section

class AutoTesterModule():
    name = "autotester"
    short = "test"
    def load_module(self):
        pass

    def unload_module(self):
        pass

    def run(self, **kwargs):
        log = Log("Autotester")
        log.info("Finding tests...")
        testsuite = unittest.TestLoader().discover('.')
        log.info("Running tests...")
        unittest.TextTestRunner(verbosity=1).run(testsuite)
        log.info("Tests done.")
        del log
        return state.ProgramExit()

        
#register to main program as a module
state.modules.append(AutoTesterModule())