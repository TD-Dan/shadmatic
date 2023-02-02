"""Advanced terminal user interface
Uses curses as terminal rendering backend
"""
from modules import ModuleBase
import state

class TermModule(ModuleBase):
    """Advanced terminal user interface
    """
    name = "terminal"
    short = "term"
    def load(self):
        super().load()
        pass

    def unload(self):
        super().unload()
        pass

#register to main program as a module
state.modules.append(TermModule())