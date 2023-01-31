"""Program help
Shows help in commandline and inside user interface on:
\t- using the program
\t- modules
\t- available tools inside modules
"""

import state

from shadowui import Section

class HelpModule():
    """Program help
    Shows help in commandline and inside user interface on:
    \t- using the program
    \t- modules
    \t- available tools inside modules
    """
    run_help = \
    """\nShadow-wallet v0.0.1 - the superboosted shimmer wallet!
    \t-h \thelp \t\tGet help
    \t-x \texec \t\tExecute a single tool command
    \t-cli \tcomline \tLaunch in simple command line input mode (CLI)
    \t-tui \tterminal \tLaunch a graphical terminal interface (TUI)\n\t\t\t\t(default if no parameters given)\n
    \t-t \ttest \t\tRun self diagnosis and tests

    \t-help more \tMore help

    \tVisit shadwallet.com for more info.
    """
    name = "help"
    short = "h"
    def load_module(self):
        pass

    def unload_module(self):
        pass

    def run(self, **kwargs):
        print(self.run_help)
        raise state.ProgramExit()

class HelpTool(Section):
    """Get help on program and tool usage"""
    short = 'h'
    long = 'help'


help_dom = [
    Section('Help',command='help', short='h')
]

#register to main program as a module
state.modules.append(HelpModule())