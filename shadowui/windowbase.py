
from .section import Section

"""Interface base class for all os level windows."""
class WindowBase(Section):    
    """Run the program main loop"""
    def run(self):
        # send load signals from leaf up, children should always be loaded first
        self.emit_signal_recursive_leaf_first("on_load")

    def add_tool(self,page): raise NotImplementedError('add_tool method not implemented by subclass.')

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)