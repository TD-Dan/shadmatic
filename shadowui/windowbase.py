
from .section import Section

"""Interface base class for all os level windows."""
class WindowBase(Section):    
    """Run the program main loop"""
    def run(self):
        #send on_load signals
        for child in self.children.values():
            child.on_load.emit()
            

    def add_tool(self,page): raise NotImplementedError('add_tool method not implemented by subclass.')

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)