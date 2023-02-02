

import state
from modules import ModuleBase


class ExecModule(ModuleBase):
    """Module command execution from cl
    Allows running any single command from any available module 
    """
    name = "exec"
    short = "e"
    help_usage = \
    """exec <module> <command> [parameter1=<> parameter2=<>]
    where:
    \tmodule\t\tModule name / module short name (f.ex. "client" or "c")
    \tcommand\t\tCommand inside module (use help <module name> for list)
    \tparameter\tParameter(s) to pass for command
    """
    def load(self):
        super().load()
        pass

    def unload(self):
        super().unload()
        pass
    
    def run_from_commandline(self, **kwargs):
        args = kwargs.get('args')
        print ("Command execution invoked with :"+str(args))

        if len(args)<2:
            raise 
        mod_name = args[1]
        com_name = args[2]
        # load module

        # exec in module

        raise state.ProgramExit()

#register to main program as a module
state.modules.append(ExecModule())