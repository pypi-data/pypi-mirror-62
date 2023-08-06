_WINDOWS = False
from typing import Tuple
from typing import Optional
import sys
try:
    import tty
    import termios
except ModuleNotFoundError:
    import msvcrt
    _WINDOWS = True
from easyansi._core.codes import CSI as _CSI
from easyansi._core.validations import validate_at_least_minimum as _validate_at_least_minimum
from easyansi._core.prnt import prnt as _prnt

MIN_COLUMN = 0
MIN_ROW = 0
MIN_MOVEMENT = 1


def up_code(rows: int = 1) -> str:
    """Return the ANSI code to move the cursor up n rows on the screen."""
    _validate_at_least_minimum(rows, MIN_MOVEMENT, "Rows up")
    return _CSI + str(rows) + "A"


def up(rows: int = 1) -> None:
    """Output the ANSI code to move the cursor up n rows on the screen."""
    _prnt(up_code(rows=rows))


def down_code(rows: int = 1) -> str:
    """Return the ANSI code to move the cursor down n rows on the screen."""
    _validate_at_least_minimum(rows, MIN_MOVEMENT, "Rows down")
    return _CSI + str(rows) + "B"


def down(rows: int = 1) -> None:
    """Output the ANSI code to move the cursor down n rows on the screen."""
    _prnt(down_code(rows=rows))


def right_code(cols: int = 1) -> str:
    """Return the ANSI code to move the cursor right n columns on the screen."""
    _validate_at_least_minimum(cols, MIN_MOVEMENT, "Columns right")
    return _CSI + str(cols) + "C"


def right(cols: int = 1) -> None:
    """Output the ANSI code to move the cursor right n columns on the screen."""
    _prnt(right_code(cols=cols))


def left_code(cols: int = 1) -> str:
    """Return the ANSI code to move the cursor left n columns on the screen."""
    _validate_at_least_minimum(cols, MIN_MOVEMENT, "Columns left")
    return _CSI + str(cols) + "D"


def left(cols: int = 1) -> None:
    """Output the ANSI code to move the cursor left n columns on the screen."""
    _prnt(left_code(cols=cols))


def locate_code(x: int, y: int) -> str:
    """Return the ANSI code to move the cursor to the x, y coordinates on the screen.
       The coordinate system is 0, 0 based."""
    _validate_at_least_minimum(x, MIN_COLUMN, "X-Coordinate")
    _validate_at_least_minimum(y, MIN_ROW, "Y-Coordinate")
    return _CSI + str(y+1) + ";" + str(x+1) + "H"


def locate(x: int, y: int) -> None:
    """Output the ANSI code to move the cursor to the x, y coordinates on the screen.
       The coordinate system is 0, 0 based."""
    _prnt(locate_code(x=x, y=y))


def hide_code() -> str:
    """Return the ANSI code to hide the cursor."""
    return _CSI + "?25l"


def hide() -> None:
    """Output the ANSI code to hide the cursor."""
    _prnt(hide_code())


def show_code() -> str:
    """Return the ANSI code to show the cursor."""
    return _CSI + "?25h"


def show() -> None:
    """Output the ANSI code to show the cursor."""
    _prnt(show_code())


def get_location() -> Tuple[int, int]:
    """Return the x, y coordinates of the cursor."""
    response = _get_location_response()
    location = response.split(";")
    x = int(location[1]) - 1
    y = int(location[0]) - 1
    return x, y


def _get_location_response() -> str:
    """Make the actual ANSI call for the cursor location.
    This code is separated out to make it easy to mock in unit tests."""
    response = ""
    _prnt(_CSI + "6n")  # Send ANSI request for cursor location
    if _WINDOWS:
        while msvcrt.kbhit():  # type: ignore
            char_in = msvcrt.getch()  # type: ignore
            response += char_in.decode("utf-8")
        response = response[2:-1]  # We do not need the first 2 bytes or the last byte
    else:
        f = sys.stdin.fileno()
        terminal_settings = termios.tcgetattr(f)  # Save terminal settings
        try:
            tty.setraw(f)
            sys.stdin.read(2)  # We do not need the first 2 bytes
            char_in = sys.stdin.read(1)
            while char_in != "R":  # R will be the last character of the ANSI response, and we don't need it
                response += char_in
                char_in = sys.stdin.read(1)  # Read a single character
        finally:
            termios.tcsetattr(f, termios.TCSADRAIN, terminal_settings)  # Restore terminal settings
    return response
