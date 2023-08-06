version = '0.9.0'

import sys, os, tempfile, platform

class Share:
    debugging = int(os.getenv('MUSICRAFT_DBG', 0))

qt_module_name = os.getenv('MUSICRAFT_QT', 'PySide2')


print(f"using version {version} of package 'musicraft'  from {os.path.split(__file__)[0]}")

dbg_print = (Share.debugging & 1) and print or (lambda *pp, **kw: None)

# locate the directory in which this file, thus package musicraft, resides
head_dir = os.path.normpath(os.path.split(__file__)[0]+ '/../')

# Depending on the install method, this may or may not also be the parent or our 'share' directory.
# There's got to be a better way, but this should work:

if head_dir.endswith('-packages'):
    head_dir = os.path.normpath(head_dir + ((platform.system()=='Windows') and '/../../' or '/../../../'))

print("head_dir....", head_dir)
temp_dir = tempfile.gettempdir()

#from .abcraft import external


if qt_module_name == 'PySide':
    from PySide import (QtCore, QtGui, QtSvg, QtWebKit)
    Signal = QtCore.Signal
    print ("using PySide!")
    name_from_dialog = lambda x:x[0]
    QtPrintSupport = QtGui
    QtWidgets = QtGui
    QtWebEngine = QtWebKit
    QtWebEngineWidgets = QtWebKit
    WebView = QtWebKit.QWebView
elif qt_module_name == 'PyQt4':
    from PyQt4 import (QtCore, QtGui, QtSvg, QtWebKit)

    Signal = QtCore.pyqtSignal
    print("using Pyqt4!")
    name_from_dialog = lambda x: x
    QtPrintSupport = QtGui
    QtWidgets = QtGui
    QtWebEngine = QtWebKit
    QtWebEngineWidgets = QtWebKit
    WebView = QtWebKit.QWebView
elif qt_module_name == 'PySide2':
    from PySide2 import (QtCore, QtGui, QtWidgets, QtPrintSupport, QtSvg, QtWebEngine, QtWebEngineWidgets)
    Signal = QtCore.Signal
    print("using PySide2!")
    name_from_dialog = lambda x: x[0]
    WebView = QtWebEngineWidgets.QWebEngineView
elif qt_module_name == 'PyQt5':
    from PyQt5 import (QtCore, QtGui, QtWidgets, QtSvg, QtPrintSupport, QtWebEngine, QtWebEngineWidgets)
    Signal = QtCore.pyqtSignal
    print("using Pyqt5!")
    name_from_dialog = lambda x:x
    WebView = QtWebEngine.QWebEngineView
else:
    raise NameError("bad value: MUSICRAFT_QT = " + qt_module_name)


class Printer(QtPrintSupport.QPrinter):
    pageSize = QtPrintSupport.QPrinter.A4

    def __init__(self):
        dbg_print ("Printer.__init__")
        QtPrintSupport.QPrinter.__init__(self, QtPrintSupport.QPrinter.HighResolution)
        self.setPageSize(self.pageSize)
        dbg_print ("!Printer.__init__")


class WithMenu(object):
    menuTag = None

    def __init__(self):
        self.printer = Printer()
        self.compositeName = 'temp'  # under review, like so much!
        self.menu = QtWidgets.QMenu(self.menuTag)
        if not (self.menuTag and self.menuItems()):
            return
        for tag, shortcut, func in self.menuItems():
            action = self.myQAction(tag, shortcut=shortcut, triggered=func)
            self.menu.addAction(action)
        Share.raft.menuBar().addMenu(self.menu)

    def menuItems(self):
        return [
        ]

    def myQAction(self, menuText, shortcut=None, triggered=None, enabled=None,
                  checkable=None, checked=None):
        action = QtWidgets.QAction(menuText, self)
        if shortcut:
            action.setShortcut(shortcut)
        if triggered:
            action.triggered.connect(triggered)
        if enabled is not None:
            action.setEnabled(enabled)
        if checkable is not None:
            action.setCheckable(checkable)
        if checked is not None:
            action.setChecked(checked)
        return action

    def printAll(self, toPDF=False):
        # fileName = self.compositeName +'.pdf'
        fileName = os.path.splitext(Share.raft.editBook.activeEdit.fileName)[0] + '.pdf'
        print(fileName)
        if toPDF:
            files = QtWidgets.QFileDialog.getSaveFileName(self,
                "write PDF to file", fileName, '*.pdf')
            fileName = files[0]
            if not fileName:
                return
        self.printer.setDocName(fileName)
        self.printer.setOutputFileName(toPDF and fileName or '')
        self.renderAll(QtGui.QPainter(self.printer))

    def renderAll(self, painter):
        self.scene().render(painter)

    def printAllToPDF(self):
        self.printAll(toPDF=True)

from .raft import *
from .abcraft import *
from .pyraft import *
# from .freqraft import *
