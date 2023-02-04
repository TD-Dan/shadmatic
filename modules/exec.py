

import state
from modules.modulebase import ModuleBase
from modules.log import Log


class ExecModule(ModuleBase):
    """Module command execution from commandline
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

    def unload(self):
        super().unload()
    
    def run_from_commandline(self, *args, **kwargs):
        runlog = Log("exec")
        runlog.info("Command execution invoked with :"+str(args))
        try:
            if len(args)<3:
                raise state.InvalidInput("No module provided. Use '-help exec' for help.")
            elif len(args)<4:
                raise state.InvalidInput("No command provided. Use '-help exec' for help.")
            mod_name = args[2]
            com_name = args[3]

            # find module
            found_module = None
            for module in state.modules:
                if module.name == mod_name or module.short == mod_name:
                    found_module = module
                    break
            if not found_module:
                raise state.InvalidInput("Can't execute from module '"+mod_name+"': no such module available.")

            # find command in module
            if not found_module.commands:
                raise state.InvalidInput("Can't execute command '"+mod_name+" "+com_name+"': module has 0 command available.")
            found_command = None
            for command in found_module.commands:
                if command.name == com_name:
                    found_command = command
                    break
            if not found_command:
                raise state.InvalidInput("Can't execute command '"+mod_name+" "+com_name+"': no such command available in the module.")
            # Test all required arguments are given
            if found_command.required_kwargs:
                for cmd,value in found_command.required_kwargs.items():
                    if not kwargs.get(cmd):
                        raise state.InvalidInput("Can't execute command '"+mod_name+" "+com_name+"': missing required argument '"+cmd+"' ("+value+")")
            
            command_method = getattr(found_module, found_command.name)

            #load module
            try:
                found_module.load()
                #execute command in module
                command_method(**kwargs)
            finally:
                found_module.unload()

        except state.InvalidInput as e:
            print(e.args[0])
            runlog.warning(e.args[0])
            raise state.ProgramCancel()
        finally:
            del runlog
        raise state.ProgramExit()

#register to main program as a module
state.modules.append(ExecModule())