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
from qgis.PyQt.QtGui import QIcon, QTextDocument
from qgis.PyQt.QtCore import pyqtSignal, Qt, QCoreApplication, QUrl
from qgis.PyQt.QtWidgets import QMessageBox, QListWidgetItem, QAbstractItemView

from qgis.core import QgsApplication
from qgis.utils import iface, OverrideCursor

from qtutor.lesson import LessonStep
from qtutor.gui.qtutorfinisheddialog import QTutorFinishedDialog

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

        self.iconEmpty = QIcon()
        self.iconCurrent = QgsApplication.getThemeIcon('/mActionArrowRight.svg')
        #self.iconCurrent = QgsApplication.getThemeIcon('/mActionStart.svg')
        #self.iconCurrent = QgsApplication.getThemeIcon('/mTaskRunning.svg')

        self.lesson = None
        self.currentStep = 0
        self.running = False

    def startLesson(self, lesson):
        self.lesson = lesson
        self.currentStep = 0
        self.running = True

        self.lstSteps.clear()
        self._restoreNextButton()

        self.lblLessonName.setText(lesson.displayName)
        for step in lesson.steps:
            item = QListWidgetItem(step.name, self.lstSteps)
            # FIXME: maybe hide automated steps?

        self._stepUp()

    def nextStep(self):
        step = self.lesson.steps[self.currentStep]
        # execute check function if any
        if step.check is not None:
            passed = step.runFunction(LessonStep.FunctionType.Check)
            if not passed:
                msg = self.tr('Looks like step was not completed. Please '
                              'complete all instructions and try again.')
                QMessageBox.warning(self, self.tr('QTutor'), msg)
                return

        # disconnect signals if any
        if step.signals is not None:
            # TODO: disconnect signals from handlers
            pass

        self.lstSteps.item(self.currentStep).setIcon(self.iconEmpty)
        self.currentStep += 1
        self._stepUp()

    def executeStep(self):
        step = self.lesson.steps[self.currentStep]
        self.setEnabled(False)
        with OverrideCursor(Qt.WaitCursor):
            step.runFunction(LessonStep.FunctionType.Execute)

        self.setEnabled(True)
        self.nextStep()

    def restartLesson(self):
        self.lstSteps.item(self.currentStep).setIcon(self.iconEmpty)
        self._restoreNextButton()

        self.currentStep = 0
        self._stepUp()

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

    def _stepUp(self):
        # this was the last step, lesson finished
        if self.currentStep == len(self.lesson.steps):
            dlg = QTutorFinishedDialog(iface.mainWindow())
            dlg.setRecommended(self.lesson.recommended)
            result = dlg.exec_()
            if result:
                self.startLesson(dlg.lesson)
            else:
                self.running = False
                self.lessonFinished.emit()
        else:
            # last but one step, change "Next" button title
            if self.currentStep == len(self.lesson.steps) - 1:
                self.btnNextStep.setText(self.tr('Finish'))

            # mark step as current and sroll list so it is visible
            item = self.lstSteps.item(self.currentStep)
            item.setIcon(self.iconCurrent)
            # TODO: highlight current step
            self.lstSteps.scrollToItem(item, QAbstractItemView.PositionAtTop)

            step = self.lesson.steps[self.currentStep]

            # connect signals if any
            if step.signals is not None:
                # TODO: connect singnals to handlers
                pass

            # load step description
            if os.path.exists(step.description):
                url = QUrl.fromUserInput(step.description)
                self.txtDescription.document().setMetaInformation(QTextDocument.DocumentUrl,
                                                                  os.path.dirname(url.toString()))
                self.txtDescription.setSource(url)
            else:
                self.txtDescription.setHtml(step.description)

            if step.prepare is not None:
                with OverrideCursor(Qt.WaitCursor):
                    step.runFunction(LessonStep.FunctionType.Prepare)

            if step.execute is not None:
                if step.type == LessonStep.StepType.Automated:
                    self.executeStep()
                else:
                    # FIXME: button state depending of existence of signals
                    self.btnExecuteStep.setEnabled(True)
            else:
                self.btnExecuteStep.setEnabled(False)

    def _restoreNextButton(self):
        self.btnNextStep.setText(self.tr('Next'))
