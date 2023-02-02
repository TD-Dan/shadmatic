

class ProgramCommand():
    """Base class for all program commands"""

    def __init__(self, name, required_kwargs, optional_kwargs) -> None:
        self.name = name
        self.required_kwargs = required_kwargs
        self.optional_kwargs = optional_kwargs