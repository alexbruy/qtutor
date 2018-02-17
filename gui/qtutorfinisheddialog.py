# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutorfinisheddialog.py
    ---------------------
    Date                 : February 2018
    Copyright            : (C) 2018 by Alexander Bruy
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
__date__ = 'February 2018'
__copyright__ = '(C) 2018, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt import uic

from qtutor import lessonsRegistry

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'ui', 'qtutorfinisheddialogbase.ui'))


class QTutorFinishedDialog(BASE, WIDGET):

    def __init__(self, parent=None):
        super(QTutorFinishedDialog, self).__init__(parent)
        self.setupUi(self)

        self.lesson = None

        self.txtRecommended.anchorClicked.connect(self.selectLesson)

    def setRecommended(self, recommended):
        if recommeneded:
            items = list()
            for lesson in recommended:
                lessonId = '{}:{}'.format(item[0], item[1])
                lesson = lessonsRegistry.lessonById(lessonId)
                if lesson:
                    items.append('<li><a href="{}">{}</a></li>'.format(lessonId, lesson.displayName))

            if items:
                text = '<ul>{}</ul>'.format(''.join(items))
                self.txtRecommended.setHtml(text)

    def selectLesson(self, url):
        self.lesson = lessonsRegistry.lessonById(url.toString())
        self.accept()
