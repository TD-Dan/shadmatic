"""Basic commandline user interface
"""
import state

from shadowui.cliwindow import CommandlineWindow
class CLIWindowModule():
    """Simple interactive CommandLine Interpreter
    """
    name = "commandline"
    short = "cli"
    def load_module(self):
        state.root += CommandlineWindow('commandline')

    def unload_module(self):
        pass

    def run(self, **kwargs):
        args = kwargs.get('args')
        print ("Commandline run invoked with :"+str(args))
        raise state.ProgramEnterInteractive()


#register to main program as a module
state.modules.append(CLIWindowModule())