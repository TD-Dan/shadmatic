
from .section import Section

class WindowBase(Section):    
    """Interface base class for all os level windows."""
    
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.enable_on_frame = False

    def on_frame(self):
        """Run the program main loop
        Needs to be implemented by child classes
        """