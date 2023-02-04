
from .section import Section,Signal

class Input(Section):
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value = value
        self._on_value_changed.emit()

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self._value = None
        self._on_value_changed = Signal()

        on_value_changed:callable = kwargs.get('on_value_changed')
        if on_value_changed:
            self._on_value_changed.connect(on_value_changed)