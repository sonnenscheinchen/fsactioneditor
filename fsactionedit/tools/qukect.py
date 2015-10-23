#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets
import pprint

fskeys = """keyboard_key_volumeup
keyboard_key_volumedown
keyboard_key_mute
keyboard_key_audionext
keyboard_key_audioprev
keyboard_key_audiostop
keyboard_key_audioplay
keyboard_key_backspace
keyboard_key_tab
keyboard_key_clear
keyboard_key_return
keyboard_key_pause
keyboard_key_escape
keyboard_key_space
keyboard_key_exclaim
keyboard_key_quotedbl
keyboard_key_hash
keyboard_key_dollar
keyboard_key_ampersand
keyboard_key_quote
keyboard_key_leftparen
keyboard_key_rightparen
keyboard_key_asterisk
keyboard_key_plus
keyboard_key_comma
keyboard_key_minus
keyboard_key_period
keyboard_key_slash
keyboard_key_0
keyboard_key_1
keyboard_key_2
keyboard_key_3
keyboard_key_4
keyboard_key_5
keyboard_key_6
keyboard_key_7
keyboard_key_8
keyboard_key_9
keyboard_key_colon
keyboard_key_semicolon
keyboard_key_less
keyboard_key_equals
keyboard_key_greater
keyboard_key_question
keyboard_key_at
keyboard_key_leftbracket
keyboard_key_backslash
keyboard_key_rightbracket
keyboard_key_caret
keyboard_key_underscore
keyboard_key_backquote
keyboard_key_a
keyboard_key_b
keyboard_key_c
keyboard_key_d
keyboard_key_e
keyboard_key_f
keyboard_key_g
keyboard_key_h
keyboard_key_i
keyboard_key_j
keyboard_key_k
keyboard_key_l
keyboard_key_m
keyboard_key_n
keyboard_key_o
keyboard_key_p
keyboard_key_q
keyboard_key_r
keyboard_key_s
keyboard_key_t
keyboard_key_u
keyboard_key_v
keyboard_key_w
keyboard_key_x
keyboard_key_y
keyboard_key_z
keyboard_key_kp0
keyboard_key_kp1
keyboard_key_kp2
keyboard_key_kp3
keyboard_key_kp4
keyboard_key_kp5
keyboard_key_kp6
keyboard_key_kp7
keyboard_key_kp8
keyboard_key_kp9
keyboard_key_kp_period
keyboard_key_kp_divide
keyboard_key_kp_multiply
keyboard_key_kp_minus
keyboard_key_kp_plus
keyboard_key_kp_enter
keyboard_key_kp_equals
keyboard_key_up
keyboard_key_down
keyboard_key_right
keyboard_key_left
keyboard_key_insert
keyboard_key_delete
keyboard_key_home
keyboard_key_end
keyboard_key_pageup
keyboard_key_pagedown
keyboard_key_f1
keyboard_key_f2
keyboard_key_f3
keyboard_key_f4
keyboard_key_f5
keyboard_key_f6
keyboard_key_f7
keyboard_key_f8
keyboard_key_f9
keyboard_key_f10
keyboard_key_f11
keyboard_key_f12
keyboard_key_f13
keyboard_key_f14
keyboard_key_f15
keyboard_key_capslock
keyboard_key_scrollock
keyboard_key_rshift
keyboard_key_lshift
keyboard_key_rctrl
keyboard_key_lctrl
keyboard_key_ralt
keyboard_key_lalt
keyboard_key_lsuper
keyboard_key_rsuper
keyboard_key_help
keyboard_key_print
keyboard_key_sysreq
keyboard_key_break
keyboard_key_menu
keyboard_key_power
keyboard_key_numlock
keyboard_key_euro
keyboard_key_undo"""


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
            self.outdict[scancode] = self.active_key.split('_')[-1]
        self.active_key = self.next_key

    def closeEvent(self, event):
        self.outdict[9] = 'escape'
        if len(self.outdict) > 1:
            with open(self.outfile, 'wt') as f:
                f.write('{0} = \n'.format(self.var_name))
                f.write(pprint.pformat(self.outdict, indent=4))
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
