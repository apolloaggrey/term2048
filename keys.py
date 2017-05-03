import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


keys = {"q": 0x10 + 0, "w": 0x10 + 1,
        "e": 0x10 + 2, "r": 0x10 + 3,
        "t": 0x10 + 4, "y": 0x10 + 5,
        "u": 0x10 + 6, "i": 0x10 + 7,
        "o": 0x10 + 8, "p": 0x10 + 9,
        "a": 0x10 + 14, "s": 0x10 + 15,
        "d": 0x10 + 16, "f": 0x10 + 17,
        "g": 0x10 + 18, "h": 0x10 + 19,
        "j": 0x10 + 20, "k": 0x10 + 21,
        "l": 0x10 + 22, "z": 0x10 + 28,
        "x": 0x10 + 29, "c": 0x10 + 30,
        "v": 0x10 + 31, "b": 0x10 + 32,
        "n": 0x10 + 33, "m": 0x10 + 34,
        ".": 0x10 + 36, "*": 0x10 + 39,
        " ": 0x10 + 41}  # "NEW_LINE": 0x10 + 0xC,


def send_key(key):
    delay = .125
    time.sleep(delay)
    PressKey(keys[key])
    time.sleep(delay)
    ReleaseKey(keys[key])
    time.sleep(delay)


if __name__ == '__main__':
    time.sleep(3)
    line = "the quick brown fox jumps over the seven lazy dogs.*"
    for char in line:
        send_key(char)
