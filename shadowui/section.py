
from enum import Enum

class Signal:
    def connect(self, handler:callable):
        self._listeners.append(handler)

    def disconnect(self, handler:callable):
        self._listeners.remove(handler)

    def emit(self,**kwargs):
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

    def __init__(self, name:str, **kwargs) -> None:
        self.name=name
        self.children:dict[str,object] = {}

        self._on_load = Signal()
        self._on_children_changed = Signal()

        children = kwargs.get('children')
        on_load:callable = kwargs.get('on_load')
        on_children_changed:callable = kwargs.get('on_children_changed')

        if children:
            self+=children
        if on_load:
            self.on_load.connect(on_load)
        if on_children_changed:
            self.on_children_changed.connect(on_children_changed)

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

    