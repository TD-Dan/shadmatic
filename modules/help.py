"""Program help
Shows help in commandline and inside user interface on:
\t- using the program
\t- modules
\t- available tools inside modules


"""

from shadowui import Section

class HelpModule():
    """Program help module
    Commandline and in-program help on:
    \t- using the program
    \t- modules
    \t- available tools inside modules
    """
    name = "help"
    short = "h"
    def load_module(self):
        pass

    def unload_module(self):
        pass

class HelpTool(Section):
    """Get help on program and tool usage"""
    short = 'h'
    long = 'help'


help_dom = [
    Section('Help',command='help', short='h')
]

#register to main program as a module
import program_state
program_state.modules.append(HelpModule())