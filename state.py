"""Globally available program state, where __main__.py and modules can share variables
Not thread safe!
"""

# main loop control exceptions
class ProgramExit(Exception):
    """Raised when program exit is requested"""
class ProgramConfirm(Exception):
    """Raised when current program state can advance or needs to be committed"""
class ProgramCancel(Exception):
    """Raised when current program state needs to be reversed"""

# Program dom root
root:object

# needs to be called absolute first in __main_.py before any modules are run
def init():
    # All loaded modules
    global modules
    modules = list[object]()
    global root
    root= None
