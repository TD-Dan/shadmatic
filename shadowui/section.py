
from enum import Enum

class Signal:
    def connect(self, handler:callable):
        """Connect a function to listen for this signal."""
        self._listeners.append(handler)

    def disconnect(self, handler:callable):
        """Disconnect a previously connected function from this signal."""
        self._listeners.remove(handler)

    def emit(self,**kwargs):
        """Call all listeners of this signal with the kwargs provided"""
        for call in self._listeners:
            call(**kwargs)

    def __init__(self) -> None:
        self._listeners:list[callable] = list()

class ListOperation(Enum):
    ADD = 1
    REMOVE = 2


class Section:

    @property 
    def on_load(self):
        return self._on_load
    @property 
    def on_children_changed(self):
        return self._on_children_changed
    @property 
    def on_frame(self):
        return self._on_frame

    def __init__(self, name:str, **kwargs) -> None:
        self.name=name
        self.children:dict[str,object] = {}

        self._on_load = Signal()
        self._on_children_changed = Signal()
        self._on_frame = Signal()

        children = kwargs.get('children')
        set_on_load:callable = kwargs.get('on_load')
        set_on_children_changed:callable = kwargs.get('on_children_changed')
        set_on_frame:callable = kwargs.get('on_frame')

        if children:
            self+=children
        if set_on_load:
            self._on_load.connect(set_on_load)
        if set_on_children_changed:
            self._on_children_changed.connect(set_on_children_changed)
        if set_on_frame:
            self._on_frame.connect(set_on_frame)

    def emit_signal_recursive_leaf_first(self,signal:str,**kwargs):
        for child in self.children.values():
            child.emit_signal_recursive_leaf_first(signal, **kwargs)
        try:
            getattr(self,signal).emit(section=self, **kwargs)
        except AttributeError:
            raise AttributeError("No Signal "+signal+" existing in "+self.name)

    def __iadd__(self, other):
        try:
            for obj in other:
                self.children[obj.name] = obj
                self._on_children_changed.emit(what=ListOperation.ADD,child=obj)
        except AttributeError:
            try:
                self.children[other.name] = other
                self._on_children_changed.emit(what=ListOperation.ADD,child=other)
            except AttributeError:
                raise TypeError
        except TypeError:
            raise TypeError("Only adding a Section or Iterable of Sections is supported")
        return self

    """Adds ability to directly access children with ['childname'] and [child.subchild.leaf] """
    def __getitem__(self,key):
        splitted = key.split('.')
        current = self
        for key in splitted:
            current = current.children[key]
        return current
    
    def print_recursive(self, section=None, level=0):
        if not section:
            section = self
        for n in range(0,level):
            print("\t", end='')
        print(str(section))
        for child in section.children.values():
            self.print_recursive(child,level+1)

    def __str__(self) -> str:
        return "< "+self.name+" >"