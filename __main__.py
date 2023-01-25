"""\nShadow-wallet v0.0.1 - the superboosted shimmer wallet!

\t-h \thelp \t\tGet help
\t-x \texec \t\tExecute a single tool command
\t-cli \tcomline \tLaunch in simple command line input mode (CLI)
\t-tui \tterminal \tLaunch a graphical terminal interface (TUI)\n
\t-t \ttest \t\tRun self diagnosis and tests

\t-help more \tMore help

\tVisit shadwallet.com for more info.
"""
__version__ = "v0.0.1"


import sys
from enum import Enum

from shadowui import Section,Input,Label

from handlers import *

program_dom = [
    Section('bootstrapper'),
    Section('header',children=[
        Section('status'),
        Section('logo',on_load=load_tools)
        ]),
    Input('prompt', on_value_changed=prompt_input),
    Section('menu'),
    Section('content'),
    Section('footer',children=[
        Label('hintline')
        ])
]

class LaunchMode(Enum):
    HELP = "help"
    TEST = "test"
    EXEC = "exec"
    CLI = "comline"
    TUI = "terminal"

def main():
    """Main entrypoint
    Selects between different user interfaces depending on comandline arguments.
    Starts the main window loop with selected UI Window.
    """
    launch_mode = LaunchMode.TUI
    mainwin = None

    try:
        args = sys.argv
        #print(sys.argv)
        if len(args)>1:
            arg1 = args[1]
            while len(arg1)>0 and arg1[0] =='-':
                arg1 = arg1[1:]
            match arg1:
                case 'h'|'help':                launch_mode = LaunchMode.HELP
                case 't'|'test':                launch_mode = LaunchMode.TEST
                case 'x'|'exec':                launch_mode = LaunchMode.EXEC
                case 'cli'|'comline':           launch_mode = LaunchMode.CLI
                case 'tui'|'terminal':          launch_mode = LaunchMode.TUI
                case _:
                    print(arg1+" is not a valid argument.\n try -help")
                    exit()
        
        match launch_mode:
            case LaunchMode.HELP:
                print(__doc__)
            case LaunchMode.TEST:
                from tests import tests
                tests()
            case LaunchMode.EXEC:
                print("Not implemented")
            case LaunchMode.CLI:
                from termwindow import CommandlineWindow
                mainwin : CommandlineWindow = CommandlineWindow('Shadow-wallet')
            case LaunchMode.TUI:
                from termwindow import TerminalWindow
                mainwin : TerminalWindow = TerminalWindow('Shadow-wallet')
    
        if mainwin:
            mainwin += program_dom
            mainwin.run()
            exit()
    except KeyboardInterrupt:
        print("User interrupted.")
        exit()


if __name__ == "__main__":
    main()