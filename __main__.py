import sys
import platform
import time
from enum import Enum
from datetime import datetime, timedelta

from modules import ModuleBase
import state
__doc__ = state.program_help_doc

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
        log.info("Program name and version: "+state.program_name+" "+state.program_version_str)
        log.info("Program started with arguments: "+str(sys.argv))
        log.info("Running on: "+str(platform.uname()._asdict()))
        log.info("Python environment: "+platform.python_implementation()+', '+platform.python_version())

        # pre-load modules (could use autodiscovery, hardcoded for now)

        import modules.help
        import modules.config
        import modules.auto_tester
        import modules.client
        #import modules.wallet
        
        import modules.exec
        import modules.cli
        import modules.term

        import modules.twitter
        #import modules.airdrop

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
                        module.run_from_commandline(args=args)
                    except state.ProgramExit:
                        raise
                    raise RuntimeError("'"+module.name+"' module run method did not raise valid program control Exception. Method must raise state.ProgramState derived response. f.ex 'raise ProgramExit()'")
        
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
        try:            
            for module in state.modules:
                if (not isinstance(module, ModuleBase)):
                    raise NotImplementedError("'"+module.name+"' module needs to be inherited from ModuleBase. f. ex. 'class MyModule(ModuleBase):'")
                module.load()
            
            last_frame = time.perf_counter_ns()
            # Main loop
            while True:
                # call all on_frame handlers
                try:
                    #loop timing
                    frame_actual = time.perf_counter_ns()
                    delta_actual = frame_actual - last_frame
                    if delta_actual < 16600000:
                        time.sleep((16600000-delta_actual)/1000000000.0) # restrain loop to 60 fps
                    else:
                        #log framedrops
                        log.warning("Main frame took longer than 1/60 seconds: "+str(delta_actual/1000000000.0)+" s")
                    frame_start = time.perf_counter_ns()
                    delta_time = frame_start - last_frame
                    last_frame = frame_start

                    #work cycle
                    state.root.emit_signal_recursive_leaf_first('on_frame',delta_ms=delta_time/1000000)

                except state.ProgramExit:
                    log.info("Normal program exit")
                    exit()
                except KeyboardInterrupt:
                    log.error("Program terminated to KeyboardInterrupt")
                    print("User interrupted.")
                    exit()
        finally:
            for module in state.modules:
                module.unload()
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