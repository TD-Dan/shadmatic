import sys
import platform
import time
import traceback
from enum import Enum
from datetime import datetime, timedelta

from modules import ModuleBase

from modules.log import Log

import state
__doc__ = state.program_help_doc

import program

def main():
    """Main entrypoint
    Selects between different user interfaces depending on comandline arguments.
    Starts the main window loop with selected UI Window.
    """
    mainlog = Log("main")
    do_interactive = False
    try:
        # Run commandline arguments interpretion and pre-load stage to determine program launch parameters
        try:
            runlog = Log("run-cli")
            argv = sys.argv
            args,kwargs = convert_lststr_to_argskwargs(argv)
            runlog.info("Program name and version: "+state.program_name+" "+state.program_version_str)
            runlog.info("Program started with arguments: "+str(sys.argv))
            runlog.info("Running on: "+str(platform.uname()._asdict()))
            runlog.info("Python environment: "+platform.python_implementation()+', '+platform.python_version())

            # pre-load modules (could use autodiscovery, hardcoded for now)

            import modules.logmodule
            import modules.help
            #import modules.config
            import modules.auto_tester
            #import modules.client
            #import modules.wallet
            
            import modules.exec
            #import modules.cli
            #import modules.term

            import modules.twitter
            #import modules.airdrop

            runlog.info("Modules pre-loaded into global program state: "+', '.join(module.name.upper() for module in state.modules))

            # Select launch module
            if len(argv)>1:
                arg1 = clean_argument(argv[1])
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
                            runlog.info("Starting module '"+module.name+"'")
                            module.run_from_commandline(*args,**kwargs)
                        except NotImplementedError:
                            print("Module '"+module.name+"' does not have commandline run capability. Try -help or -exec commands.")
                            raise state.ProgramExit()
                        except state.ProgramExit:
                            raise
                        raise RuntimeError("'"+module.name+"' module run method did not raise valid program control Exception. Method must raise state.ProgramState derived response. f.ex 'raise ProgramExit()'")
            
            print(arg1+" is not a valid command. use -help to get started")
            runlog.info(arg1+" is not a valid command.")
            raise state.ProgramExit()
        
        except KeyboardInterrupt:
            runlog.error("Program terminated to KeyboardInterrupt")
            print("User interrupted.")
        except state.ProgramEnterInteractive:
            do_interactive = True
        finally:
            del runlog
        

        if do_interactive:
            # Selected run module requested interactive mode
            # Entering full program mode
            mainlog.info("Entered Interactive program mode")
            mainlog.info("Loading all modules")
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
                            mainlog.warning("Main frame took longer than 1/60 seconds: "+str(delta_actual/1000000000.0)+" s")
                        frame_start = time.perf_counter_ns()
                        delta_time = frame_start - last_frame
                        last_frame = frame_start

                        #work cycle
                        state.root.emit_signal_recursive_leaf_first('on_frame',delta_ms=delta_time/1000000)

                    except state.ProgramExit:
                        mainlog.info("Normal program exit")
                        raise
                    except KeyboardInterrupt:
                        mainlog.error("Program terminated to KeyboardInterrupt")
                        print("User interrupted.")
                        raise state.ProgramExit()
            finally:
                for module in state.modules:
                    module.unload()
                    
    except state.ProgramCancel:
        mainlog.info("Program run was cancelled")
    except state.ProgramExit:
        mainlog.info("Program run exitted normally")
    except Exception as e:
        print("Abnormal program exit!")
        mainlog.error("Abnormal program exit")
        trace = traceback.format_exc()
        mainlog.error(trace)
    finally:
        del mainlog
    exit()

    
def clean_argument(str:str) -> str:
    """Remove preceding '-' marks from arguments"""
    while len(str)>0 and str[0] =='-':
        str = str[1:]
    return str

def convert_lststr_to_argskwargs(argv) -> list[tuple,dict]:
    args = []
    kwargs = {}
    for arg in argv:
        index = arg.find('=')
        if index < 0:
            args.append(arg)
        else:
            kwargs[arg[:index]]=arg[index+1:]
    return [args,kwargs]

if __name__ == "__main__":
    main()
