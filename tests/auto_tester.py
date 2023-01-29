import unittest

from shadowui import Log
    
def run():
    log = Log("Autotester")
    log.info("Finding tests...")
    testsuite = unittest.TestLoader().discover('.')
    log.info("Running tests...")
    unittest.TextTestRunner(verbosity=1).run(testsuite)
    log.info("Tests done.")
    del log