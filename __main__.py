"""\nShadow-wallet v0.0.1 - the superboosted shimmer wallet!

\t-h \thelp \t\tGet help
\t-x \texec \t\tExecute a single tool command
\t-cli \tcomline \tLaunch in simple command line input mode (CLI)
\t-tui \tterminal \tLaunch a graphical terminal interface (TUI)\n\t\t\t\t(default if no parameters given)\n
\t-t \ttest \t\tRun self diagnosis and tests

\t-help more \tMore help

\tVisit shadwallet.com for more info.
"""
__version__ = "v0.0.1"

import sys
import platform
from enum import Enum

import program_state
program_state.init()

from program import *

def main():
    """Main entrypoint
    Selects between different user interfaces depending on comandline arguments.
    Starts the main window loop with selected UI Window.
    """
    clean_exit = False

    try:
        # always use logger module
        import modules.log
        log = modules.log.Log("main")
        args = sys.argv
        log.info("Program started with arguments: "+str(sys.argv))
        log.info("Running on: "+str(platform.uname()._asdict()))
        log.info("Python environment: "+platform.python_implementation()+', '+platform.python_version())

        # preload modules (could use autodiscovery, hardcoded for now)

        import modules.help
        import modules.config
        #import modules.auto_unittest
        #import modules.client
        #import modules.wallet
        #import modules.airdrop
        import modules.cli
        import modules.term

        log.info("modules pre-loaded in global program state: "+', '.join(module.name for module in program_state.modules))

        # Select launch module
        launch = modules.help #default

        if len(args)>1:
            arg1 = strip_decorators(args[1])
        else:
            la

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
                print("hlep")
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
                mainwin : CommandlineWindow = CommandlineWindow('Shadow-wallet',args=args)
            case LaunchMode.TUI:
                from termwindow import TerminalWindow
                mainwin : TerminalWindow = TerminalWindow('Shadow-wallet',args=args)
    
        if mainwin:
            mainwin += program_dom
            mainwin.actionmap = ACTION
            mainwin.run()
            raise ProgramExit()
    except ProgramExit:
        log.info("Normal program exit")
        #print("Exit ok.")
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
    
def strip_decorators(str:str) -> str:
    while len(str)>0 and str[0] =='-':
        str = str[1:]
    return str

if __name__ == "__main__":
    main()