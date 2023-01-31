"""Advanced terminal user interface
Uses curses as terminal rendering backend
"""
import state

class TermModule():
    """Advanced terminal user interface
    """
    name = "terminal"
    short = "term"
    def load_module(self):
        pass

    def unload_module(self):
        pass

#register to main program as a module
state.modules.append(TermModule())