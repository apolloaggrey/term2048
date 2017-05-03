# -*- coding: UTF-8 -*-

# Common values

# Space Bar key to pause the game
SPACE = 32
# Undo last move back
UNDO = 117

# Vim keys
K, J, L, H = 107, 106, 108, 104
A, S, D, W, U = 97, 115, 100, 119, 117

try:
    import termios
except ImportError:
    # Windows

    import msvcrt

    UP, DOWN, RIGHT, LEFT = 72, 80, 77, 75

    __key_aliases = {
        K: UP,
        W: UP,
        J: DOWN,
        S: DOWN,
        L: RIGHT,
        D: RIGHT,
        H: LEFT,
        A: LEFT,
        U: UNDO,
    }

    def getKey():
        while True:
            if msvcrt.kbhit():
                a = ord(msvcrt.getch())
                return __key_aliases.get(a, a)

else:
    # Linux/OSX

    # refs:
    # http://bytes.com/topic/python/answers/630206-check-keypress-linux-xterm
    # http://stackoverflow.com/a/2521032/735926

    import sys
    import tty

    __fd = sys.stdin.fileno()
    __old = termios.tcgetattr(__fd)

    # Arrow keys
    # they are preceded by 27 and 91, hence the double 'if' in getKey.
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    __key_aliases = {
        K: UP,
        W: UP,
        J: DOWN,
        S: DOWN,
        L: RIGHT,
        D: RIGHT,
        H: LEFT,
        A: LEFT,
    }

    def __getKey():
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch) if ch else None
        finally:
            termios.tcsetattr(__fd, termios.TCSADRAIN, __old)

    def getKey():
        """
        same as __getKey, but handle arrow keys
        """
        k = __getKey()
        if k == 27:
            k = __getKey()
            if k == 91:
                k = __getKey()

        return __key_aliases.get(k, k)

# legacy support
getArrowKey = getKey
