

from .section import Section

class PageView(Section):
    """Multipage view that shows its each children on its own page. Can have pagenumber or tabbing behaviors."""
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)