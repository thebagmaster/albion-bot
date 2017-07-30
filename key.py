import ctypes
import win32process
from ctypes import *
from ctypes.wintypes import *

from time import sleep

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class Key:
    def __init__(self):
        _ = {}
        _["ESCAPE"] = 0x01
        _["1"] = 0x02
        _["2"] = 0x03
        _["3"] = 0x04
        _["4"] = 0x05
        _["5"] = 0x06
        _["6"] = 0x07
        _["7"] = 0x08
        _["8"] = 0x09
        _["9"] = 0x0A
        _["0"] = 0x0B
        _["MINUS"] = 0x0C    # - on main keyboard
        _["EQUALS"] = 0x0D
        _["BACK"] = 0x0E    # backspace
        _["TAB"] = 0x0F
        _["Q"] = 0x10
        _["W"] = 0x11
        _["E"] = 0x12
        _["R"] = 0x13
        _["T"] = 0x14
        _["Y"] = 0x15
        _["U"] = 0x16
        _["I"] = 0x17
        _["O"] = 0x18
        _["P"] = 0x19
        _["LBRACKET"] = 0x1A
        _["RBRACKET"] = 0x1B
        _["RETURN"] = 0x1C    # Enter on main keyboard
        _["LCONTROL"] = 0x1D
        _["A"] = 0x1E
        _["S"] = 0x1F
        _["D"] = 0x20
        _["F"] = 0x21
        _["G"] = 0x22
        _["H"] = 0x23
        _["J"] = 0x24
        _["K"] = 0x25
        _["L"] = 0x26
        _["SEMICOLON"] = 0x27
        _["APOSTROPHE"] = 0x28
        _["GRAVE"] = 0x29    # accent grave
        _["LSHIFT"] = 0x2A
        _["BACKSLASH"] = 0x2B
        _["Z"] = 0x2C
        _["X"] = 0x2D
        _["C"] = 0x2E
        _["V"] = 0x2F
        _["B"] = 0x30
        _["N"] = 0x31
        _["M"] = 0x32
        _["COMMA"] = 0x33
        _["PERIOD"] = 0x34    # . on main keyboard
        _["SLASH"] = 0x35    # / on main keyboard
        _["RSHIFT"] = 0x36
        _["MULTIPLY"] = 0x37    # * on numeric keypad
        _["LMENU"] = 0x38    # left Alt
        _["SPACE"] = 0x39
        _["CAPITAL"] = 0x3A
        _["F1"] = 0x3B
        _["F2"] = 0x3C
        _["F3"] = 0x3D
        _["F4"] = 0x3E
        _["F5"] = 0x3F
        _["F6"] = 0x40
        _["F7"] = 0x41
        _["F8"] = 0x42
        _["F9"] = 0x43
        _["F10"] = 0x44
        _["NUMLOCK"] = 0x45
        _["SCROLL"] = 0x46    # Scroll Lock
        _["NUMPAD7"] = 0x47
        _["NUMPAD8"] = 0x48
        _["NUMPAD9"] = 0x49
        _["SUBTRACT"] = 0x4A    # - on numeric keypad
        _["NUMPAD4"] = 0x4B
        _["NUMPAD5"] = 0x4C
        _["NUMPAD6"] = 0x4D
        _["ADD"] = 0x4E    # + on numeric keypad
        _["NUMPAD1"] = 0x4F
        _["NUMPAD2"] = 0x50
        _["NUMPAD3"] = 0x51
        _["NUMPAD0"] = 0x52
        _["DECIMAL"] = 0x53    # . on numeric keypad
        _["F11"] = 0x57
        _["F12"] = 0x58
        _["F13"] = 0x64    #                     (NEC PC98)
        _["F14"] = 0x65    #                     (NEC PC98)
        _["F15"] = 0x66    #                     (NEC PC98)
        _["KANA"] = 0x70    # (Japanese keyboard)
        _["CONVERT"] = 0x79    # (Japanese keyboard)
        _["NOCONVERT"] = 0x7B    # (Japanese keyboard)
        _["YEN"] = 0x7D    # (Japanese keyboard)
        _["NUMPADEQUALS"] = 0x8D    # = on numeric keypad (NEC PC98)
        _["CIRCUMFLEX"] = 0x90    # (Japanese keyboard)
        _["AT"] = 0x91    #                     (NEC PC98)
        _["COLON"] = 0x92    #                     (NEC PC98)
        _["UNDERLINE"] = 0x93    #                     (NEC PC98)
        _["KANJI"] = 0x94    # (Japanese keyboard)
        _["STOP"] = 0x95    #                     (NEC PC98)
        _["AX"] = 0x96    #                     (Japan AX)
        _["UNLABELED"] = 0x97    #                        (J3100)
        _["NUMPADENTER"] = 0x9C    # Enter on numeric keypad
        _["RCONTROL"] = 0x9D
        _["NUMPADCOMMA"] = 0xB3    # , on numeric keypad (NEC PC98)
        _["DIVIDE"] = 0xB5    # / on numeric keypad
        _["SYSRQ"] = 0xB7
        _["RMENU"] = 0xB8    # right Alt
        _["HOME"] = 0xC7    # Home on arrow keypad
        _["UP"] = 0xC8    # UpArrow on arrow keypad
        _["PRIOR"] = 0xC9    # PgUp on arrow keypad
        _["LEFT"] = 0xCB    # LeftArrow on arrow keypad
        _["RIGHT"] = 0xCD    # RightArrow on arrow keypad
        _["END"] = 0xCF    # End on arrow keypad
        _["DOWN"] = 0xD0    # DownArrow on arrow keypad
        _["NEXT"] = 0xD1    # PgDn on arrow keypad
        _["INSERT"] = 0xD2    # Insert on arrow keypad
        _["DELETE"] = 0xD3    # Delete on arrow keypad
        _["LWIN"] = 0xDB    # Left Windows key
        _["RWIN"] = 0xDC    # Right Windows key
        _["APPS"] = 0xDD    # AppMenu key
        _["BACKSPACE"] = _["BACK"]            # backspace
        _["NUMPADSTAR"] = _["MULTIPLY"]        # * on numeric keypad
        _["LALT"] = _["LMENU"]           # left Alt
        _["CAPSLOCK"] = _["CAPITAL"]         # CapsLock
        _["NUMPADMINUS"] = _["SUBTRACT"]        # - on numeric keypad
        _["NUMPADPLUS"] = _["ADD"]             # + on numeric keypad
        _["NUMPADPERIOD"] = _["DECIMAL"]         # . on numeric keypad
        _["NUMPADSLASH"] = _["DIVIDE"]          # / on numeric keypad
        _["RALT"] = _["RMENU"]           # right Alt
        _["UPARROW"] = _["UP"]              # UpArrow on arrow keypad
        _["PGUP"] = _["PRIOR"]           # PgUp on arrow keypad
        _["LEFTARROW"] = _["LEFT"]            # LeftArrow on arrow keypad
        _["RIGHTARROW"] = _["RIGHT"]           # RightArrow on arrow keypad
        _["DOWNARROW"] = _["DOWN"]            # DownArrow on arrow keypad
        _["PGDN"] = _["NEXT"]            # PgDn on arrow keypad
        _["ENTER"] = _["RETURN"]            # PgDn on arrow keypad
        self._ = _
        self.pressed = {}
        self.SendInput = ctypes.windll.user32.SendInput

    def Toggle(self,key):
        if key :
            key = key.upper()
            if key in self._ :
                if key in self.pressed :
                    self.pressed.pop(key, None)
                    self.ReleaseKey(self._[key])
                else:
                    self.pressed[key] = True
                    self.PressKey(self._[key])

    def Press(self,key):
        if key :
            key = key.upper()
            if key in self._ :
                self.PressKey(self._[key])

    def Release(self,key):
        if key :
            key = key.upper()
            if key in self._ :
                self.ReleaseKey(self._[key])

    def KeyStroke(self,key):
        if key :
            key = key.upper()
            #print (key)
            if key in self._ :
                self.PressKey(self._[key])
                sleep(0.03)
                self.ReleaseKey(self._[key])

    def PressKey(self,hexKeyCode):
        if hexKeyCode != 0x0 :
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
            x = Input( ctypes.c_ulong(1), ii_ )
            self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def ReleaseKey(self,hexKeyCode):
        if hexKeyCode != 0x0 :
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
            x = Input( ctypes.c_ulong(1), ii_ )
            self.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
