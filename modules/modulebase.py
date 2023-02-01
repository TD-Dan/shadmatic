


class ModuleBase():
    """Base class for all program modules"""
    name:str = None
    """Name of the module, lowercase and consisting only of letters,numbers and '_'"""
    short:str = None
    """Shorthand name of the module consisting only of max 4 letters"""

    commands = None
    """List of commands available by the modules exec function"""

    def load(self):
        """Run when program enters interactive mode (if program has enabled this module)"""
        raise NotImplementedError("load method not implemented in '"+self.name+"' module.")

    def unload(self):
        """Called when program unloads this module or leaves interactive mode"""
        raise NotImplementedError("unload method not implemented in '"+self.name+"' module.")

    def run(self, **kwargs):
        """Called when this module gets invoked from the commandline as programs 1st argument.
        kwargs contain 'args' with all commandline arguments, and can be accessed with args = kwargs.get('args')."""
        raise NotImplementedError("run method not implemented in '"+self.name+"' module.")

    def exec(self,command, **kwargs):
        """Execute a command within the module, passing kwargs to it"""
        raise NotImplementedError("exec method not implemented in '"+self.name+"' module.")
