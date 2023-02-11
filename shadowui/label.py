
from helper.stringtool import xstr

from .section import Section

class Label(Section):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        
        self.pre_content = kwargs.get('pre_content')
        self.content = kwargs.get('content')
        self.post_content = kwargs.get('post_content')

    def get_all_content(self) -> str:
        return xstr(self.pre_content)+xstr(self.content)+xstr(self.post_content)