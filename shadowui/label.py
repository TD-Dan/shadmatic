
from .section import Section

class Label(Section):
    content = None
    pre_content = None
    post_content = None
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)