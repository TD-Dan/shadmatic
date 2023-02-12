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

    def unload(self):
        super().unload()

    def run_from_commandline(self, *args, **kwargs):
        self.use_color = kwargs.get('color')
        if self.use_color:
            match self.use_color.lower():
                case 'y'|'yes'|'true':
                    self.use_color = True
                case 'n'|'no'|'not'|'false'|'none':
                    self.use_color = False
                case _:
                    raise state.InvalidInput("yes/no expcected, got "+self.use_color)
        else:
            self.use_color = False
        raise state.ProgramEnterInteractive()
    
#register to main program as a module
state.modules.append(TermModule())