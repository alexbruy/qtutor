# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutordock.py
    ---------------------
    Date                 : December 2017
    Copyright            : (C) 2017 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'December 2017'
__copyright__ = '(C) 2017, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'ui', 'qtutordockbase.ui'))


class QTutorDock(BASE, WIDGET):

    lessonFinished = pyqtSignal()

    def __init__(self, parent=None):
        super(QTutorDock, self).__init__(parent)
        self.setupUi(self)

        self.btnNextStep.clicked.connect(self.nextStep)
        self.btnExecuteStep.clicked.connect(self.executeStep)
        self.btnRestartLesson.clicked.connect(self.restartLesson)
        self.btnQuitLesson.clicked.connect(self.quitLesson)

        self.running = False

    def nextStep(self):
        pass

    def executeStep(self):
        pass

    def restartLesson(self):
        pass

    def quitLesson(self):
        if self.running:
            reply = QMessageBox.question(None,
                                         self.tr('Lesson is not completed!'),
                                         self.tr('Current lesson is not completed. '
                                                 'Do you want to finish it and return '
                                                 'to the QTutor library?'))
            if reply == QMessageBox.Yes:
                self.running = False
                self.lessonFinished.emit()
