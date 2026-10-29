from enum import StrEnum


class ANSI(StrEnum):

    ESC              = "\x1b"

    CLEAR            = f"{ESC}[2J"
    CLEAR_BACKGROUND = f"{ESC}[49m"
    CLEAR_FOREGROUND = F"{ESC}[39m"

    ARROW_UP         = f"{ESC}[A"
    ARROW_DOWN       = f"{ESC}[B"
    ARROW_RIGHT      = f"{ESC}[C"
    ARROW_LEFT       = f"{ESC}[D"

    CTRL_UP          = f"{ESC}[1;5A"
    CTRL_DOWN        = f"{ESC}[1;5B"
    CTRL_RIGHT       = f"{ESC}[1;5C"
    CTRL_LEFT        = f"{ESC}[1;5D"

    SHOW_CURSOR      = f"{ESC}[?25h"
    HIDE_CURSOR      = f"{ESC}[?25l"

    START_SYNC       = f"{ESC}[?2025h"
    END_SYNC         = f"{ESC}[?2025l"

    ENTER_ALT_SCREEN = f"{ESC}[?1049h"
    EXIT_ALT_SCREEN  = f"{ESC}[?1049l"

    ENABLE_FOCUS     = f"{ESC}[?1004h"
    DISABLE_FOCUS    = f"{ESC}[?1004l"

    DEFAULT_CURSOR   = f"{ESC}[0 q"
    BLINKING_BLOCK   = f"{ESC}[1 q"
    BLINKING_UNDER   = f"{ESC}[3 q"
    BLINKING_BAR     = f"{ESC}[5 q"
    STEADY_BLOCK     = f"{ESC}[2 q"
    STEADY_UNDER     = f"{ESC}[4 q"
    STEADY_BAR       = f"{ESC}[6 q"
