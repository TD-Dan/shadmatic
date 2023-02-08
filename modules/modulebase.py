
from modules.log import Log

class ModuleException(Exception): pass
class ModuleAlreadyLoaded(ModuleException): pass
class ModuleAlreadyUnLoaded(ModuleException): pass

modlog = None
modlog_refs = 0

class ModuleBase():
    """Base class for all program modules"""
    name:str = "None"
    """Name of the module, lowercase and consisting only of letters,numbers and '_'"""
    short:str = ''
    """Shorthand name of the module consisting only of max 4 letters"""

    commands = None
    """List of commands available by the modules exec function"""

    loaded = False

    def load(self):
        """Run when program enters interactive mode (if program has enabled this module).
        Needs to be called by inheriting classes."""
        if self.loaded:
            name = "ModuleBase"
            if self.name:
                name = self.name
            raise ModuleAlreadyLoaded("Module '"+name+"' is already loaded!")
        self.loaded = True
        
        global modlog
        global modlog_refs
        if not modlog:
            modlog = Log('module')
        modlog_refs += 1
        modlog.info("Loading module '"+self.name+"'")

    def unload(self):
        """Called when program unloads this module or leaves interactive mode.
        Needs to be called by inheriting classes."""
        if not self.loaded:
            name = "ModuleBase"
            if self.name:
                name = self.name
            raise ModuleAlreadyUnLoaded("Module '"+name+"' is already unloaded!")
        self.loaded = False
        
        global modlog
        global modlog_refs
        modlog.info("Unloading module '"+self.name+"'")
        modlog_refs -= 1
        if modlog_refs <= 0:
            del modlog

    def run_from_commandline(self, *args, **kwargs):
        """Called when this module gets invoked from the commandline as programs 1st argument.
        HOX! The load method has not been called at this point! load gets only called if entering ProgramInteractive mode.
        Args and kwargs contain all commandline arguments"""
        raise NotImplementedError("run method not implemented in '"+self.name+"' module.")

    def exec(self, command, **kwargs):
        """Execute a command within the module, passing kwargs to it
        Default behavior is to search requested command from self.commands and call a method with the same name.
        Does not need to be implemented by inheriting classes."""
        if self.commands:
            for program_command in self.commands:
                if program_command.name == command:
                    command_method = getattr(self, command)
                    command_method(**kwargs)
            else:
                #print("Module '"+self.name+"' has no commands implemented")
                raise NotImplementedError("Module '"+self.name+"' has no command '"+command+"' implemented")
        else:
            #print("Module '"+self.name+"' has no commands implemented")
            raise NotImplementedError("Module '"+self.name+"' has no commands implemented")
