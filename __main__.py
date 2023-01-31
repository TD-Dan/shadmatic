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

import state
state.init()

from program import *

def main():
    """Main entrypoint
    Selects between different user interfaces depending on comandline arguments.
    Starts the main window loop with selected UI Window.
    """
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

        log.info("modules pre-loaded in global program state: "+', '.join(module.name for module in state.modules))

        # Select launch module

        if len(args)>1:
            arg1 = clean_argument(args[1])
        else:
            arg1 = 'help'

        for module in state.modules:
            match arg1:
                case module.name | module.short:
                    module.load_module()
                    module.run(args=args)
            raise state.ProgramExit()
        
        print(arg1+" is not a valid command. use -help to get started")
        # match launch_mode:
        #     case LaunchMode.HELP:
        #         print("hlep")
        #         raise ProgramExit()
        #     case LaunchMode.TEST:
        #         from tests import auto_tester
        #         auto_tester.run()
        #         raise ProgramExit()
        #     case LaunchMode.EXEC:
        #         print("Not implemented")
        #         raise ProgramExit()
        #     case LaunchMode.CLI:
        #         from termwindow import CommandlineWindow
        #         mainwin : CommandlineWindow = CommandlineWindow('Shadow-wallet',args=args)
        #     case LaunchMode.TUI:
        #         from termwindow import TerminalWindow
        #         mainwin : TerminalWindow = TerminalWindow('Shadow-wallet',args=args)
    
        # if mainwin:
        #     mainwin += program_dom
        #     mainwin.actionmap = ACTION
        #     mainwin.run()
        #     raise ProgramExit()
    except state.ProgramExit:
        log.info("Normal program exit")
        #print("Exit ok.")
    except KeyboardInterrupt:
        log.error("Program terminated to KeyboardInterrupt")
        print("User interrupted.")
    except:
        log.error("Abnormal program exit")
        print("Abnormal program exit!")
        raise
    finally:
        #cleanup
        del log
    
def clean_argument(str:str) -> str:
    """Remove preceding '-' marks from arguments"""
    while len(str)>0 and str[0] =='-':
        str = str[1:]
    return str

if __name__ == "__main__":
    main()