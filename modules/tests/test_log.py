import unittest

from modules.log import Log, LOG_LEVEL
from modules.log import log_history

class TestLogging(unittest.TestCase):
    def setUp(self):
        self.testlog = Log("TestLog")
        self.testlog.echo_level = LOG_LEVEL.NONE

    def tearDown(self):
        del self.testlog

    def test_log_add(self):
        
        self.testlog.error("Error1")
        self.testlog.info("Info1")
        self.testlog.warning("Warning1")
        self.testlog.warning("Warning2")
        self.testlog.error("Error2")
        self.testlog.info("Info2")
        self.testlog.error("Error3")
        self.testlog.info("Info3")
        self.testlog.warning("Warning3")

        self.assertEqual(log_history[-3].str,"Error3")
        self.assertEqual(log_history[-2].str,"Info3")
        self.assertEqual(log_history[-1].str,"Warning3")

    logger_calls = [0,0,0]
    def loglistener1(self,str,**kwargs): self.logger_calls[0]+=1
    def loglistener2(self,str,**kwargs): self.logger_calls[1]+=1
    def loglistener3(self,str,**kwargs): self.logger_calls[2]+=1

    def test_log_listeners(self):
        self.testlog.add_listener(self.loglistener1)
        self.testlog.add_listener(self.loglistener2)
        self.testlog.add_listener(self.loglistener3)
        self.testlog.error("LError1")
        self.testlog.warning("LWarning1")
        self.testlog.info("LInfo1")

        self.assertEqual(self.logger_calls[0],3)
        self.assertEqual(self.logger_calls[1],3)
        self.assertEqual(self.logger_calls[2],3)
        
    def test_log_exceptions(self):
        try:
            raise TypeError("Exception1")
        except TypeError as e:
            self.testlog.error("EError1",exception=e)
        try:
            raise TypeError("Exception2")
        except TypeError as e:
            self.testlog.warning("EWarning1",exception=e)