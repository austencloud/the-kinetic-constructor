class BaseGlyph:
    """Base class for all glyphs to define a common interface."""
    name: str
    
    def __init__(self, name: str):
        self.name = name
