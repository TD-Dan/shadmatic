"""Globally available program state, where __main__.py and modules can share variables
Not thread safe!
"""

# main program control exceptions

class ProgramState(Exception):
    """Base class for all Program state changes"""
    
class ProgramExit(ProgramState):
    """Raised when program exit is requested"""
class ProgramConfirm(ProgramState):
    """Raised when current program state can advance or needs to be committed"""
class ProgramCancel(ProgramState):
    """Raised when current program state needs to be reversed"""
class ProgramEnterInteractive(ProgramState):
    """Raised when module requests interactive mode
    Results in all modules getting loaded"""

# needs to be called absolute first in __main_.py before any modules are run
#def init():
    # All loaded modules
#global modules
modules = list[object]()
#global root
root= None
