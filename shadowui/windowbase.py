
from .section import Section

class WindowBase(Section):    
    """Interface base class for all os level windows."""
    
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)