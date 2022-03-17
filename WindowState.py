from enum import Enum

class WindowState(Enum):
    """Denotes state of the window"""
    MAXIMIZED = 1
    MINIMIZED = 2
    RESTORED = 3