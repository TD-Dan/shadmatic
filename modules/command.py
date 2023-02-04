

class ProgramCommand():
    """Base class for all program commands"""

    def __init__(self, name, help=None, required_kwargs=None, optional_kwargs=None) -> None:
        self.name = name
        if help: self.__doc__ = help
        self.required_kwargs = required_kwargs
        self.optional_kwargs = optional_kwargs