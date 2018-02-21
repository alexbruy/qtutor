# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutoroptionswidget.py
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
from qgis.PyQt.QtWidgets import QHBoxLayout

from qgis.gui import QgsFileWidget, QgsOptionsPageWidget
from qgis.core import QgsApplication, QgsSettings

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'qtutoroptionswidgetbase.ui'))


class QTutorOptionsPage(QgsOptionsPageWidget):
    def __init__(self, parent):
        super(QTutorOptionsPage, self).__init__(parent)
        self.widget = QTutorOptionsWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setMargin(0)
        self.setLayout(layout)
        layout.addWidget(self.widget)
        self.setObjectName('qtutorOptions')

    def apply(self):
        self.widget.accept()

    def helpKey(self):
        return ''


class QTutorOptionsWidget(BASE, WIDGET):
    def __init__(self, parent=None):
        super(QTutorOptionsWidget, self).__init__(parent)
        self.setupUi(self)

        self.widgetLessonsPath.setFileWidgetButtonVisible(True)
        self.widgetLessonsPath.setStorageMode(QgsFileWidget.GetDirectory)
        self.widgetLessonsPath.setDialogTitle(self.tr('Select directory'))

        lessonsPath = QgsSettings().value('qtutor/lessonsPath',
                                          os.path.join(QgsApplication.qgisSettingsDirPath(), 'lessons'))
        self.widgetLessonsPath.setFilePath(lessonsPath)

    def accept(self):
        QgsSettings().value('qtutor/lessonsPath', self.widgetLessonsPath.filePath())
