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
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QDockWidget, QMessageBox, QTreeWidgetItem

from qgis.gui import QgsGui
from qgis.core import QgsSettings, QgsApplication
from qgis.utils import iface, OverrideCursor

from qtutor import lessonsRegistry
from qtutor.gui.qtutordock import QTutorDock

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'ui', 'qtutorlibrarydialogbase.ui'))


class QTutorLibraryDialog(BASE, WIDGET):
    def __init__(self, parent=None):
        super(QTutorLibraryDialog, self).__init__(parent)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)

        self.btnAddLessons.clicked.connect(self.addLessons)
        self.btnRemoveLessons.clicked.connect(self.removeLessons)
        self.btnStartLesson.clicked.connect(self.startLesson)

        self.treeLessons.itemExpanded.connect(self.updateIcon)
        self.treeLessons.itemCollapsed.connect(self.updateIcon)

        self.iconExpanded = QgsApplication.getThemeIcon('/mActionFileOpen.svg')
        self.iconCollapsed = QIcon(os.path.join(pluginPath, 'icons', 'folderClosed.svg'))

        self.dock = QTutorDock()
        self.dock.lessonFinished.connect(self.showLibrary)

        self.populateTree()

    def addLessons(self):
        settings = QgsSettings()
        lastDirectory = settings.value('qtutor/lastLessonDirectory', os.path.expanduser('~'), str)
        fileName, _ = QgsFileDialog.getOpenFileName(self,
                                                    self.tr('Select file'),
                                                    lastDirectory,
                                                    self.tr('ZIP archives (*.zip *.ZIP)')
                                                   )
        if fileName:
            with OverrideCursor(Qt.WaitCursor):
                settings.setValue('qtutor/lastLessonDirectory', os.path.dirname(fileName))
                lessonsRegistry.installLessons(fileName)
                self.populateTree()

    def removeLessons(self):
        item = self.treeLessons.currentItem()
        # TODO: get lesson from item and uninstall it
        #lessonsRegistry.uninstallLesson()

    def startLesson(self):
        if self.dock.running:
            reply = QMessageBox.warning(self,
                                        self.tr('Lesson already running!'),
                                        self.tr('Can not start lesson as there is '
                                        'already running one. Please finish active '
                                        'lesson and try again.'))
            return

        area = QgsSettings().value('qtutor/dockArea', Qt.RightDockWidgetArea)
        iface.addDockWidget(area, self.dock)
        self.showMinimized()

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
            groupItem = QTreeWidgetItem(self.treeLessons)
            groupItem.setText(0, groupName)
            groupItem.setIcon(0, self.iconCollapsed)
            groupItem.setData(0, Qt.UserRole, groupId)
            for lessonId, lesson in lessonsRegistry.lessons[groupId].items():
                lessonItem = QTreeWidgetItem(groupItem)
                lessonItem.setText(0, lesson.displayName)
                lessonItem.setData(0, Qt.UserRole, lessonId)

            self.treeLessons.addTopLevelItem(groupItem)

    def updateIcon(self, item):
        if item.isExpanded():
            item.setIcon(0, self.iconExpanded)
        else:
            item.setIcon(0, self.iconCollapsed)
