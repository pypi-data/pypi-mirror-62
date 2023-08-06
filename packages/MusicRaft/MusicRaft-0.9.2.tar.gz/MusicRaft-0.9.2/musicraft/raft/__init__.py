#!/usr/bin/python3
"""
Copyright 2016 Hippos Technical Systems BV.

@author: larry
"""
import sys
from .editbook import EditBook
from .. import (Shared, QtCore, QtWidgets, WithMenu, dbg_print)
from .external import (StdOut, StdErr)
#import qdarkstyle

class StdBook(QtWidgets.QTabWidget):
    headerText = 'error/diagnostic output'
    whereDockable   = QtCore.Qt.AllDockWidgetAreas
    whereToDock = QtCore.Qt.LeftDockWidgetArea

    def __init__(self, dock=None):
        QtWidgets.QTabWidget.__init__(self)

class DisplayBook(QtWidgets.QTabWidget):
    headerText = 'styled output'
    whereDockable   = QtCore.Qt.AllDockWidgetAreas
    whereToDock = QtCore.Qt.RightDockWidgetArea

    def __init__(self, dock=None):
        QtWidgets.QTabWidget.__init__(self)


class Dock(QtWidgets.QDockWidget):
    def __init__(self, widgetClass, visible=True):
        QtWidgets.QDockWidget.__init__(self, widgetClass.headerText)
        self.setAllowedAreas(widgetClass.whereDockable)
        self.widget = widgetClass(dock=self)
        self.setWidget(self.widget)
        self.setVisible(visible)


class Raft(QtWidgets.QMainWindow, WithMenu):
    menuTag = '&File'

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Shared.raft = self
        #self.resize(1024, 768)
        self.editBookDock = Dock(EditBook, True)
        self.addDockWidget(EditBook.whereToDock, self.editBookDock)
        self.editBook = self.editBookDock.widget
        self.stdBook = Dock(StdBook,  True)
        self.stdBook.setMinimumHeight(420)
        self.addDockWidget(StdBook.whereToDock, self.stdBook)
        self.stdBook.setMinimumHeight(180)
        sys.stdout = StdOut()
        sys.stderr = StdErr()
        print ("testing stdout...", file=sys.stdout)
        print ("testing stderr...", file=sys.stderr)
        self.createMenus()
        self.displayBookDock = Dock(DisplayBook)
        self.displayBook = self.displayBookDock.widget
        self.addDockWidget(DisplayBook.whereToDock, self.displayBookDock)
        WithMenu.__init__(self)


    def start(self):
        self.show()
        try:
            self.editBook.openThemAll(sys.argv[1:], force=True)
        except FileNotFoundError:
            print("warning: couldn't open initial file(s)!", file=sys.stderr)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About 'Raft'",
                "<p>To be updated!.</p>"
                "<p></p>")

    def createMenus(self):
        self.helpMenu = QtWidgets.QMenu("&Help", self)
        self.aboutAct = self.myQAction("About &Raft", triggered=self.about)
        self.aboutQtAct = self.myQAction("About &Qt", triggered=QtWidgets.qApp.aboutQt)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.helpAction = self.menuBar().addMenu(self.helpMenu)

    def closeEvent(self, e):
        self.editBook.exit_etc()

    def menuItems(self):
        return [
                    ('&New',           'Ctrl+N', self.editBook.newFile,),
                    ('&Open',          'Ctrl+O', self.editBook.loadAnyFile,),
                    ('&Close',         'Ctrl+C', self.editBook.closeFile,),
                    #('Open in new &Instance', 'Ctrl+I', self.editor.cloneAnyFile,),
                    ('&Reload',        'Ctrl+R', self.editBook.reloadFile,),
                    ('R&estart',       'Ctrl+E', self.editBook.restart,),
                    ('&Save',          'Ctrl+S', self.editBook.saveFile,),
                    ('Save &As',       'Ctrl+A', self.editBook.saveFileAs,),
                    ('E&xit',          'Ctrl+Q', self.editBook.exit_etc),
                    ('&Transpose',     'Ctrl+T', self.editBook.transpose,),
        ]
