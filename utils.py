# -*- coding: utf-8 -*-

"""
***************************************************************************
    utils.py
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
import shutil
import tempfile

from qgis.utils import iface


def tempDirectory():
    tmpPath = os.path.join(tempfile.gettempdir(), 'qtutor')
    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)

    return tmpPath


def clearTempData():
    shutil.rmtree(tempDirectory(), True)


def menuByName(menuString):
    menuPath = menuString.split('|')

    menuAction = None
    actions = iface.mainWindow().menuBar().actions()
    for action in actions:
        if action.text().replace('&', '') == menuPath[0]:
            menuAction = action
            if len(menuPath) > 1:
                menuAction = findMenuItem(menuPath, action, 1)
            break

    return menuAction


def findMenuItem(menuPath, subMenu, level):
    menuAction = None

    if subMenu.text().replace('&', '') == menuPath[level]:
        menuAction = subMenu
        if len(menuPath) >  level + 1:
            menuAction = findMenuItem(menuPath, subMenu, level + 1)
    else:
        actions = subMenu.menu().actions()
        for action in actions:
            if action.text().replace('&', '') == menuPath[level]:
                menuAction = action
                if len(menuPath) > level + 1:
                    menuAction = findMenuItem(menuPath, action, level + 1)
                break
    return menuAction


def isLesson(dirName):
    return os.path.isdir(dirName) and os.path.isfile(os.path.join(dirName, "lesson.yaml"))
