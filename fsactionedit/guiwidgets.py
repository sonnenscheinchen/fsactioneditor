from PyQt5 import QtCore, QtGui, QtWidgets


class AmigaSubActionComboBox(QtWidgets.QComboBox):

    SUBACTION_NUMBER = 0

    def __init__(self, parent):
        super().__init__(parent)
        AmigaSubActionComboBox.SUBACTION_NUMBER += 1
        self._subaction_number = AmigaSubActionComboBox.SUBACTION_NUMBER

    @property
    def subaction_number(self):
        return self._subaction_number


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.menuFile = QtWidgets.QMenu("&File", self)
        self.menuHelp = QtWidgets.QMenu("&Help", self)

        self.acnew = QtWidgets.QAction("&New Configuration", self.parent)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.acnew.setIcon(icon)
        self.acload = QtWidgets.QAction("&Load Configuration...", self.parent)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.acload.setIcon(icon)
        self.acsave = QtWidgets.QAction("&Save Configuration", self.parent)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.acsave.setIcon(icon)
        self.acsave.setDisabled(True)
        self.acsaveas = QtWidgets.QAction(
            "Save Configuration &as...", self.parent)
        icon = QtGui.QIcon.fromTheme("document-save-as")
        self.acsaveas.setIcon(icon)
        self.acquit = QtWidgets.QAction("&Quit", self.parent)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.acquit.setIcon(icon)
        self.accim = QtWidgets.QAction("Custom Input &Mapping", self.parent)
        icon = QtGui.QIcon.fromTheme("help-browser")
        self.accim.setIcon(icon)
        self.acia = QtWidgets.QAction("&Input Actions", self.parent)
        icon = QtGui.QIcon.fromTheme("help-browser")
        self.acia.setIcon(icon)
        self.aca = QtWidgets.QAction("&About", self.parent)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.aca.setIcon(icon)
        self.menuFile.addAction(self.acnew)
        self.menuFile.addAction(self.acload)
        self.menuFile.addAction(self.acsave)
        self.menuFile.addAction(self.acsaveas)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.acquit)
        self.menuHelp.addAction(self.accim)
        self.menuHelp.addAction(self.acia)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.aca)
        self.addAction(self.menuFile.menuAction())
        self.addAction(self.menuHelp.menuAction())


class JoyCaptureButton(QtWidgets.QPushButton):

    sig = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCheckable(True)

    def keyReleaseEvent(self, event):
        if self.isChecked() is True:
            scancode = event.nativeScanCode()
            self.sig.emit(scancode)
