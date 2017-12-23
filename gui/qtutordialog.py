# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutordialog.py
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
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtCore import QUrl, QSettings, QLocale
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox,
                                )
from qgis.gui import QgsGui


pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'qtutordialogbase.ui'))


class QTutorDialog(BASE, WIDGET):
    def __init__(self, parent=None):
        super(QTutorDialog, self).__init__(parent)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)

        self.btnAddLessons.clicked.connect(self.addLessons)
        self.btnRemoveLessons.clicked.connect(self.removeLessons)
        self.btnStartLesson.clicked.connect(self.startLesson)

    def addLessons(self):
        pass

    def removeLessons(self):
        pass

    def startLesson(self):
        pass

    def reject(self):
        QDialog.reject(self)
