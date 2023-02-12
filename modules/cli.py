"""Basic commandline user interface
"""

from modules import ModuleBase
import state

from shadowui.cliwindow import CommandlineWindow

class CLIModule(ModuleBase):
    """Simple interactive commandline interpreter
    Simplest way of invoking full program capabilities in an interactive session."""
    name = "commandline"
    short = "cli"
    
    help_usage = \
    """cli [color=<yes/no>]
    where:
    \tcolor=\tEnable colored output, valid values:
    \t\tyes (default)
    \t\tno"""

    create_window = False

    def load(self):
        super().load()
        if self.create_window:
            state.root += CommandlineWindow('cliwindow',use_color=self.use_color)

    def unload(self):
        super().unload()
        pass

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
        self.create_window=True
        raise state.ProgramEnterInteractive()

#register to main program as a module
state.modules.append(CLIModule())