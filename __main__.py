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
import time
from enum import Enum

import state

import program

def main():
    """Main entrypoint
    Selects between different user interfaces depending on comandline arguments.
    Starts the main window loop with selected UI Window.
    """

    try:
        # Run commandline arguments interpretion and pre-load stage to determine program launch parameters

        # always use logger module
        import modules.log
        log = modules.log.Log("main")
        args = sys.argv
        log.info("Program started with arguments: "+str(sys.argv))
        log.info("Running on: "+str(platform.uname()._asdict()))
        log.info("Python environment: "+platform.python_implementation()+', '+platform.python_version())

        # pre-load modules (could use autodiscovery, hardcoded for now)

        import modules.help
        import modules.config
        import modules.auto_tester
        import modules.client
        #import modules.wallet
        #import modules.airdrop
        import modules.cli
        import modules.term

        log.info("Modules pre-loaded into global program state: "+', '.join(module.name.upper() for module in state.modules))

        # Select launch module
        if len(args)>1:
            arg1 = clean_argument(args[1])
        else:
            arg1 = 'help'

        # Initialize state
        from shadowui.section import Section
        state.root = Section('root')
        state.root += program.program_dom

        # Run selected module
        for module in state.modules:
            match arg1:
                case module.name | module.short:
                    try:
                        module.run(args=args)
                    except state.ProgramExit:
                        raise
                    raise RuntimeError("Module loader did not return valid state.ProgramState control Exception.")
        
        print(arg1+" is not a valid command. use -help to get started")
        log.info(arg1+" is not a valid command.")
        raise state.ProgramExit()

    except state.ProgramExit:
        log.info("Normal program exit")
        #print("Exit ok.")
        exit()
    except KeyboardInterrupt:
        log.error("Program terminated to KeyboardInterrupt")
        print("User interrupted.")
        exit()

    except state.ProgramEnterInteractive:

        # Selected run module requested interactive mode
        # Entering full program mode

        log.info("Enter Interactive mode")
        log.info("Loading all modules")
        
        for module in state.modules:
            module.load_module()
        
        # Main loop
        while True:
            # call all on_frame handlers
            try:
                time.sleep(0.02) # restrain loop to 50 fps
            except state.ProgramExit:
                log.info("Normal program exit")
                exit()
            except KeyboardInterrupt:
                log.error("Program terminated to KeyboardInterrupt")
                print("User interrupted.")
                exit()
    except:
        log.error("Abnormal program exit")
        print("Abnormal program exit!")
        raise
    finally:
        #cleanup
        #state.root.print_recursive()
        del log
    
def clean_argument(str:str) -> str:
    """Remove preceding '-' marks from arguments"""
    while len(str)>0 and str[0] =='-':
        str = str[1:]
    return str

if __name__ == "__main__":
    main()