#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets
import pprint

# grep FS_ML_KEY_ $SRCDIR/libfsemu/src/ml/sdl2_keys.h \
# | cut -c 15- | cut -d , -f 1

fskeys = """A
B
C
D
E
F
G
H
I
J
K
L
M
N
O
P
Q
R
S
T
U
V
W
X
Y
Z
1
2
3
4
5
6
7
8
9
0
RETURN
ESCAPE
BACKSPACE
TAB
SPACE
MINUS
EQUALS
LEFTBRACKET
RIGHTBRACKET
BACKSLASH
SEMICOLON
QUOTE
BACKQUOTE
COMMA
PERIOD
SLASH
CAPSLOCK
F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12
PRINT
SCROLLOCK
PAUSE
INSERT
HOME
PAGEUP
DELETE
END
PAGEDOWN
RIGHT
LEFT
DOWN
UP
NUMLOCK
KP_DIVIDE
KP_MULTIPLY
KP_MINUS
KP_PLUS
KP_ENTER
KP1
KP2
KP3
KP4
KP5
KP6
KP7
KP8
KP9
KP0
KP_PERIOD
LESS
MENU
MUTE
VOLUMEUP
VOLUMEDOWN
SYSREQ
LCTRL
LSHIFT
LALT
LSUPER
RCTRL
RSHIFT
RALT
RSUPER
MUTE"""


class CaptureTool(QtWidgets.QMainWindow):

    def __init__(self, outfile, var_name='all_hostactions'):
        super().__init__()
        self.var_name = var_name
        self.outfile = outfile
        self.outdict = {}
        self.all_keys_gen = iter(fskeys.split())
        self.active_key = next(self.all_keys_gen)
        self.next_key = None
        self.cw = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.cw)
        self.resize(460, 200)
        self.setWindowTitle('QUKECT - Quite Ugly Key Event Capture Tool')
        self.lbkey = QtWidgets.QLabel(self.active_key)
        self.lbmsg = QtWidgets.QLabel("""
            Hello, I'm QUKECT.
            Please press the following keys on your keyboard.
            If you don't know what a specific key is, just press Esc.
            I am smart and I already know the keycode for Esc.

        """)
        self.vl = QtWidgets.QVBoxLayout(self.cw)
        self.vl.addWidget(self.lbmsg)
        self.vl.addWidget(self.lbkey)

    def keyReleaseEvent(self, event):
        try:
            self.next_key = next(self.all_keys_gen)
        except StopIteration:
            self.close()
            return  # why!?
        self.lbkey.setText(self.next_key)
        scancode = event.nativeScanCode()
        if scancode == 9:
            print('Skipped key ', self.active_key)
        else:
            print(scancode, self.active_key)
            self.outdict[scancode] = self.active_key.lower()
        self.active_key = self.next_key

    def closeEvent(self, event):
        self.outdict[9] = 'escape'
        if len(self.outdict) > 1:
            with open(self.outfile, 'wt') as f:
                f.write('{0} = \n'.format(self.var_name))
                f.write(pprint.pformat(self.outdict, indent=4,  width=5))
            print('wrote ', self.outfile)
        event.accept()

if __name__ == '__main__':
    try:
        outfile = sys.argv[1]
    except IndexError:
        print('Usage: {0} <outputfile>\n\
            Warning! This file will be overwritten.'.format(sys.argv[0]))
        quit()
    app = QtWidgets.QApplication(sys.argv)
    ct = CaptureTool(outfile=outfile)
    ct.show()
    sys.exit(app.exec_())
