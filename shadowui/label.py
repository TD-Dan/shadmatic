
from .section import Section

class Label(Section):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        
        self.pre_content = kwargs.get('pre_content')
        self.content = kwargs.get('content')
        self.post_content = kwargs.get('post_content')