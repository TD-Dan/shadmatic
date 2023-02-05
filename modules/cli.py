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
        state.root += CommandlineWindow('commandline', on_frame=test_on_frame)

    def unload(self):
        super().unload()
        pass

    def run_from_commandline(self, *args, **kwargs):
        print ("Commandline run invoked with :"+str(args))
        color = kwargs.get('color')
        raise state.ProgramEnterInteractive()

def test_on_frame(section, delta_ms):
    print(section.name+" got on_frame, delta milliseconds: "+str(delta_ms))

#register to main program as a module
state.modules.append(CLIModule())