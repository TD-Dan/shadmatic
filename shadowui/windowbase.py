
from .section import Section

class WindowBase(Section):    
    """Interface base class for all os level windows."""
    def run(self):
        """Run the program main loop"""
        # send load signals from leaf up, children should always be loaded first
        self.emit_signal_recursive_leaf_first("on_load")

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)