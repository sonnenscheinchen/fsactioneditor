import json
from PyQt5 import QtCore
from string import digits, ascii_lowercase


class JoyCapture(QtCore.QProcess):

    eventsig = QtCore.pyqtSignal(str)
    HAT_STATES = {1: 'up', 2: 'right', 4: 'down', 8: 'left'}

    def __init__(self, parent):
        super().__init__(parent)

        self.devices = {}
        self.timer = QtCore.QTimer(parent=self)
        self.timer.setInterval(3000)
        self.timer.setSingleShot(True)
        self.setProgram('fs-uae-device-helper')
        self.setArguments(['--events'])
        self.readyRead.connect(self.__process_output)
        self.started.connect(self.timer.start)
        self.finished.connect(self.timer.stop)
        # self.error.connect(self.on_error) # FIXME

    @QtCore.pyqtSlot()
    def __process_output(self):
        data = self.readAllStandardOutput().data()
        if self.timer.isActive() is True:
            events = data.decode().splitlines()
        else:
            # we should already have all joystick names now.
            # use only last event, this is much faster
            events = (data.decode().splitlines()[-1],)

        for line in events:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            jtype = event.get('type', '')
            if jtype == 'joy-device-added':
                device = self.__convert_device_name(event.get('name'))
                self.devices[event.get('device')] = device
                continue

            device = self.devices.get(event.get('device'))

            if jtype == 'joy-button-up':
                buttonno = event.get('button')
                self.eventsig.emit('{0}_button_{1}'.format(device, buttonno))
            elif jtype == 'joy-axis-motion':
                state = event.get('state')
                if state < -20000:
                    direction = 'neg'
                elif state > 20000:
                    direction = 'pos'
                else:
                    continue
                axisno = event.get('axis')
                self.eventsig.emit('{0}_axis_{1}_{2}'.format(
                    device, axisno, direction))
            elif jtype == 'joy-hat-motion':
                hatno = event.get('hat')
                state = event.get('state')
                if state not in self.HAT_STATES.keys():
                    continue
                direction = self.HAT_STATES.get(state)
                self.eventsig.emit('{0}_hat_{1}_{2}'.format(
                    device, hatno, direction))

    def __convert_device_name(self, name):
        return ''.join([i if i in ascii_lowercase +
                        digits else '_' for i in name.lower()])

    def enable(self):
        self.start()

    def disable(self):
        self.timer.stop()
        self.terminate()
