
class ModuleException(Exception): pass
class ModuleAlreadyLoaded(ModuleException): pass
class ModuleAlreadyUnLoaded(ModuleException): pass

class ModuleBase():
    """Base class for all program modules"""
    name:str = None
    """Name of the module, lowercase and consisting only of letters,numbers and '_'"""
    short:str = None
    """Shorthand name of the module consisting only of max 4 letters"""

    commands = None
    """List of commands available by the modules exec function"""

    loaded = False

    def load(self):
        """Run when program enters interactive mode (if program has enabled this module)"""
        if self.loaded:
            name = "ModuleBase"
            if self.name:
                name = self.name
            raise ModuleAlreadyLoaded("Module '"+name+"' is already loaded!")
        self.loaded = True

    def unload(self):
        """Called when program unloads this module or leaves interactive mode"""
        if not self.loaded:
            name = "ModuleBase"
            if self.name:
                name = self.name
            raise ModuleAlreadyUnLoaded("Module '"+name+"' is already unloaded!")
        self.loaded = False

    def run_from_commandline(self, **kwargs):
        """Called when this module gets invoked from the commandline as programs 1st argument.
        HOX! The load method has not been called at this point! load gets only called if entering ProgramInteractive mode.
        kwargs contain 'args' with all commandline arguments, and can be accessed with args = kwargs.get('args')."""
        raise NotImplementedError("run method not implemented in '"+self.name+"' module.")

    def exec(self,command, **kwargs):
        """Execute a command within the module, passing kwargs to it"""
        raise NotImplementedError("exec method not implemented in '"+self.name+"' module.")
