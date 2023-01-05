#TODO: I NEED TO ADD GETTERS AND SETTERS FOR Y AND X BECAUSE THEY NEED unicurses.touchwin(self.parent.win)
#TODO: I NEED TO CHECK FOR WRITE/READ/EXECUTE PERMISSIONS (PREVENT EXCEPTIONS\ERRORS)

from .file_manager import TUIFIManager
from .utils import BEGIN_MOUSE, END_MOUSE

from typing import Final

__all__ = (
    "__version__",
    "TUIFIManager",
    "BEGIN_MOUSE",
    "END_MOUSE",
)
__version__: Final[str] = "2.3.4"

"""
- 2022-12-19 01:15:32 AM REMINDER: THE REASON WHY I USED self.position.iy INSTEAD OF self.iy IS BECAUSE CHANGING IT THAT WAY DOESN'T REDRAW THE WINDOW
- 2022-12-21 08:23:25 PM REMINDER: What if i rename .. folder?
"""
