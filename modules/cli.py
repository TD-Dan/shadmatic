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
    
    def load(self):
        super().load()
        state.root += CommandlineWindow('cliwindow')

    def unload(self):
        super().unload()
        pass

    def run_from_commandline(self, *args, **kwargs):
        print ("Commandline run invoked with :"+str(args))
        color = kwargs.get('color')
        raise state.ProgramEnterInteractive()

#register to main program as a module
state.modules.append(CLIModule())