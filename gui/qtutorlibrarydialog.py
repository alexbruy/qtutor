# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutorlibrarydialog.py
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
from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import QIcon, QTextDocument
from qgis.PyQt.QtWidgets import QDialog, QDockWidget, QMessageBox, QTreeWidgetItem, QFileDialog

from qgis.gui import QgsGui
from qgis.core import QgsSettings, QgsApplication
from qgis.utils import iface, OverrideCursor

from qtutor import lessonsRegistry
from qtutor.gui.qtutordock import QTutorDock

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'ui', 'qtutorlibrarydialogbase.ui'))


class QTutorLibraryDialog(BASE, WIDGET):

    GROUP_ITEM = QTreeWidgetItem.UserType
    LESSON_ITEM = QTreeWidgetItem.UserType + 1

    def __init__(self, parent=None):
        super(QTutorLibraryDialog, self).__init__(parent)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)

        self.btnAddLessons.clicked.connect(self.addLessons)
        self.btnRemoveLessons.clicked.connect(self.removeLessons)
        self.btnStartLesson.clicked.connect(self.startLesson)

        self.treeLessons.itemExpanded.connect(self.updateIcon)
        self.treeLessons.itemCollapsed.connect(self.updateIcon)
        self.treeLessons.currentItemChanged.connect(self.updateInformation)

        self.iconExpanded = QgsApplication.getThemeIcon('/mIconFolderOpen.svg')
        self.iconCollapsed = QgsApplication.getThemeIcon('/mIconFolder.svg')
        self.iconLesson = QIcon(os.path.join(pluginPath, 'icons', 'lesson.svg'))

        self.dock = QTutorDock()
        self.dock.lessonFinished.connect(self.showLibrary)

        self.btnStartLesson.setEnabled(False)

        self.populateTree()

    def addLessons(self):
        settings = QgsSettings()
        lastDirectory = settings.value('qtutor/lastLessonDirectory', os.path.expanduser('~'), str)
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  self.tr('Select file'),
                                                  lastDirectory,
                                                  self.tr('ZIP archives (*.zip *.ZIP)')
                                                 )
        if fileName:
            with OverrideCursor(Qt.WaitCursor):
                settings.setValue('qtutor/lastLessonDirectory', os.path.dirname(fileName))
                lessonsRegistry.installLessonsFromZip(fileName)
                self.populateTree()

    def removeLessons(self):
        with OverrideCursor(Qt.WaitCursor):
            lessonId = self.treeLessons.currentItem().data(0, Qt.UserRole)
            lessonsRegistry.uninstallLesson(lessonId)
            self.populateTree()

    def startLesson(self):
        if self.dock.running:
            reply = QMessageBox.warning(self,
                                        self.tr('Lesson already running!'),
                                        self.tr('Can not start lesson as there is '
                                        'already running one. Please finish active '
                                        'lesson and try again.'))
            return

        lesson = lessonsRegistry.lessonById(self.treeLessons.currentItem().data(0, Qt.UserRole))
        if lesson:
            area = QgsSettings().value('qtutor/dockArea', Qt.RightDockWidgetArea)
            iface.addDockWidget(area, self.dock)
            self.showMinimized()
            self.dock.startLesson(lesson)

    def showLibrary(self):
        iface.removeDockWidget(self.dock)
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def reject(self):
        QDialog.reject(self)

    def populateTree(self):
        self.treeLessons.clear()

        for groupId, groupName in lessonsRegistry.groups.items():
            groupItem = QTreeWidgetItem(self.treeLessons, self.GROUP_ITEM)
            groupItem.setText(0, groupName)
            groupItem.setData(0, Qt.DecorationRole, self.iconCollapsed)
            groupItem.setData(0, Qt.UserRole, groupId)
            for lessonId, lesson in lessonsRegistry.lessons[groupId].items():
                lessonItem = QTreeWidgetItem(groupItem, self.LESSON_ITEM)
                lessonItem.setText(0, lesson.displayName)
                lessonItem.setData(0, Qt.DecorationRole, self.iconLesson)
                lessonItem.setData(0, Qt.UserRole, lessonId)

            self.treeLessons.addTopLevelItem(groupItem)

    def updateIcon(self, item):
        if item.isExpanded():
            item.setData(0, Qt.DecorationRole, self.iconExpanded)
        else:
            item.setData(0, Qt.DecorationRole, self.iconCollapsed)

    def updateInformation(self, current, previous):
        if current is None or current.type() == self.GROUP_ITEM:
            self.txtInfo.clear()
            self.btnStartLesson.setEnabled(False)
        else:
            lesson = lessonsRegistry.lessonById(current.data(0, Qt.UserRole))
            if lesson:
                if os.path.exists(lesson.description):
                    url = QUrl.fromUserInput(lesson.description)
                    self.txtInfo.document().setMetaInformation(QTextDocument.DocumentUrl,
                                                               os.path.dirname(url.toString()))
                    self.txtInfo.setSource(url)
                else:
                    self.txtInfo.setHtml(lesson.description)

                self.btnStartLesson.setEnabled(True)
