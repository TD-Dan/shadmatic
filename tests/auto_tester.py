import unittest
    
def run():
    print("Starting autotester...")
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)