

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
        pass

    def unload(self):
        pass
    
    def run(self, **kwargs):
        args = kwargs.get('args')
        print ("Command execution invoked with :"+str(args))
        raise state.ProgramExit()

#register to main program as a module
state.modules.append(ExecModule())