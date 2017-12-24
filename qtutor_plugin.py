# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutor_plugin.py
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

from qgis.PyQt.QtCore import (QCoreApplication, QLocale, QTranslator)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.gui import QgsOptionsWidgetFactory
from qgis.core import QgsSettings, QgsApplication

from qtutor.gui.qtutorlibrarydialog import QTutorLibraryDialog
from qtutor.gui.qtutoroptionswidget import QTutorOptionsPage
from qtutor.gui.aboutdialog import AboutDialog

pluginPath = os.path.dirname(__file__)


class QTutorOptionsFactory(QgsOptionsWidgetFactory):

    def __init__(self):
        super(QgsOptionsWidgetFactory, self).__init__()

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'qtutor.png'))

    def createWidget(self, parent):
        return QTutorOptionsPage(parent)


class QTutorPlugin:
    def __init__(self, iface):
        self.iface = iface

        overrideLocale = QgsSettings().value('locale/overrideFlag', False, bool)
        if not overrideLocale:
            locale = QLocale.system().name()[:2]
        else:
            locale = QgsSettings().value('locale/userLocale', '')

        qmPath = '{}/i18n/qtutor_{}.qm'.format(pluginPath, locale)

        if os.path.exists(qmPath):
            self.translator = QTranslator()
            self.translator.load(qmPath)
            QCoreApplication.installTranslator(self.translator)

        self.optionsFactory = QTutorOptionsFactory()
        self.optionsFactory.setTitle(self.tr('QTutor'))
        iface.registerOptionsWidgetFactory(self.optionsFactory)

    def initGui(self):
        self.actionRun = QAction(
            self.tr('QTutor'), self.iface.mainWindow())
        self.actionRun.setIcon(
            QIcon(os.path.join(pluginPath, 'icons', 'qtutor.png')))
        self.actionRun.setObjectName('runQTutor')

        self.actionAbout = QAction(
            self.tr('About QTutor…'), self.iface.mainWindow())
        self.actionAbout.setIcon(
            QgsApplication.getThemeIcon('/mActionHelpContents.svg'))
        self.actionRun.setObjectName('aboutQTutor')

        self.iface.addPluginToMenu(self.tr('QTutor'), self.actionRun)
        self.iface.addPluginToMenu(self.tr('QTutor'), self.actionAbout)
        self.iface.addToolBarIcon(self.actionRun)

        self.actionRun.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

    def unload(self):
        self.iface.removePluginMenu(self.tr('QTutor'), self.actionRun)
        self.iface.removePluginMenu(self.tr('QTutor'), self.actionAbout)
        self.iface.removeToolBarIcon(self.actionRun)

        self.iface.unregisterOptionsWidgetFactory(self.optionsFactory)

    def run(self):
        dlg = QTutorLibraryDialog()
        dlg.show()
        dlg.exec_()

    def about(self):
        d = AboutDialog()
        d.exec_()

    def tr(self, text):
        return QCoreApplication.translate('QTutor', text)
