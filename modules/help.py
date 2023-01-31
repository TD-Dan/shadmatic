"""Program help
Shows help in commandline and inside user interface on:
\t- using the program
\t- modules
\t- available tools inside modules
"""

import state

from shadowui import Section


help_page = [
    Section('Help')
]

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
    help_usage = \
    """help <topic>"""
    name = "help"
    short = "h"
    def load_module(self):
        content = state.root['content']
        content += help_page
        pass

    def unload_module(self):
        pass

    def run(self, **kwargs):
        args = kwargs.get('args')
        if len(args)>2:
            #print("display help for "+args[2])
            for module in state.modules:
                match args[2]:
                    case module.name | module.short:
                        if module.__doc__:
                            print("\nModule: \t"+module.name.capitalize())
                            print("Short command: \t"+module.short+"\n")
                            if hasattr(module, '__doc__'):
                                print(module.__doc__)
                            if hasattr(module, 'help_usage'):
                                print("Usage: \t"+module.help_usage)
                        else:
                            print("No help available for module "+module.name)
                        raise state.ProgramExit()
                
            print("No help found for '"+args[2]+"'")
            raise state.ProgramExit()
        else:
            print(self.run_help)
        raise state.ProgramExit()


#register to main program as a module
state.modules.append(HelpModule())