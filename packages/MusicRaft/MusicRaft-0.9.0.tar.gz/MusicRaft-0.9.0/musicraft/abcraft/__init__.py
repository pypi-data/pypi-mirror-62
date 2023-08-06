#!/usr/bin/python
"""
Copyright 2015 Hippos Technical Systems BV.

@author: larry
"""
import os
from .. import (Share, QtWidgets, Printer, dbg_print, version)
from .score import Score
from .syntax import AbcHighlighter

from .external import (Abc2midi, Abcm2svg, Abc2abc)

from .midiplayer import MidiPlayer


class AbcRaft(object):

    def __init__(self):
        Share.abcRaft = self
        self.score = Score()
        self.abc2abc = Abc2abc()
        self.abc2midi = Abc2midi()
        self.abcm2svg = Abcm2svg()

        self.printer = Printer()

        Share.raft.setWindowTitle(f"Musicraft version {version}")
        Share.raft.displayBook.addTab(self.score, "Score")
        #Share.raft.displayBook.setFixedWidth(800)
        Share.raft.editBook.fileLoaded.connect(self.checkLoadedFile)

        self.midiPlayer = MidiPlayer()

    def checkLoadedFile(self, editor, filename):
        dbg_print('checkLoadedFile', filename)
        if os.path.splitext(filename)[1] in ('.abc', '.ABC'):
            dbg_print("we expect ABC syntax in " + filename)
            editor.highlighter = syntax.AbcHighlighter(editor.document(), editor)

        Share.raft.menuBar().show()
