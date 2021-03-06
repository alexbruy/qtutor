# -*- coding: utf-8 -*-

"""
***************************************************************************
    functions.py
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
import uuid

from qgis.utils import iface

import qtutor.utils as utils


def loadProject(projectPath):
    root = os.path.dirname(projectPath)
    fileName = os.path.basename(projectPath)
    tmp = os.path.join(utils.tempDirectory(), uuid.uuid4().hex)
    shutil.copytree(root, tmp)
    iface.addProject(os.path.join(tmp, fileName))
