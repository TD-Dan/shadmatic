"""Basic commandline user interface
"""
import state

class CliModule():
    """Basic commandline user interface
    """
    name = "commandline"
    short = "cli"
    def load_module(self):
        pass

    def unload_module(self):
        pass

#register to main program as a module
state.modules.append(CliModule())