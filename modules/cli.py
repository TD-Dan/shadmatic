"""Basic commandline user interface
"""
import program_state

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
program_state.modules.append(CliModule())