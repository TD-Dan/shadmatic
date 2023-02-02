"""Automatic unittesting"""
import unittest

import state

from modules import ModuleBase
from modules.log import Log

from shadowui import Section

class TestOutputStream():
    def __init__(self,logger:Log) -> None:
        self.logger = logger
        self.buffer = ''

    def write(self, str):
        self.buffer += str
    
    def flush(self):
        self.logger.info(self.buffer)
        print(self.buffer, end='',flush=True)
        self.buffer = ''

class AutoTesterModule(ModuleBase):
    """Program integrity testing suite"""
    name = "autotester"
    short = "test"
    def load(self):
        super().load()
        self.log = Log("Autotester")
        pass

    def unload(self):
        super().unload()
        self.log.info("!!!! HERE")
        del self.log

    def run_from_commandline(self, **kwargs):
        self.load()
        output_logger = TestOutputStream(self.log)
        self.log.info("Finding tests...")
        testsuite = unittest.TestLoader().discover('.')
        self.log.info("Running tests...")
        unittest.TextTestRunner(stream=output_logger, verbosity=1).run(testsuite)
        self.log.info("Tests done.")
        self.unload()
        raise state.ProgramExit()

        
#register to main program as a module
state.modules.append(AutoTesterModule())