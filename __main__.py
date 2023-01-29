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

from shadowui import Log, ProgramExit
from program import *

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
    log = Log("main")
    clean_exit = False

    try:
        args = sys.argv
        log.info("Program started with arguments: "+str(sys.argv))
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
                    log.error(arg1+" is not a valid argument.\n try -help")
                    raise ProgramExit()
        
        match launch_mode:
            case LaunchMode.HELP:
                print(__doc__)
                raise ProgramExit()
            case LaunchMode.TEST:
                from tests import auto_tester
                auto_tester.run()
                raise ProgramExit()
            case LaunchMode.EXEC:
                print("Not implemented")
                raise ProgramExit()
            case LaunchMode.CLI:
                from termwindow import CommandlineWindow
                mainwin : CommandlineWindow = CommandlineWindow('Shadow-wallet')
            case LaunchMode.TUI:
                from termwindow import TerminalWindow
                mainwin : TerminalWindow = TerminalWindow('Shadow-wallet')
    
        if mainwin:
            mainwin += program_dom
            mainwin.actionmap = ACTION
            mainwin.run()
            raise ProgramExit()
    except ProgramExit:
        log.info("Normal program exit")
        print("Exit ok.")
        clean_exit = True
    except KeyboardInterrupt:
        log.error("Program terminated to KeyboardInterrupt")
        print("User interrupted.")
        clean_exit = True
    
    if not clean_exit:
        log.error("Abnormal program exit")
        print("Abnormal program exit!")

    #cleanup
    del log
    

if __name__ == "__main__":
    main()