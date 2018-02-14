# -*- coding: utf-8 -*-

"""
***************************************************************************
    qtutorregistry.py
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

from qgis.core import QgsApplication, QgsSettings

from qtutor.lesson import Lesson
from qtutor import utils


class QTutorRegistry:

    def __init__(self):
        self.lessons = list()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(QTutorRegistry, cls).__new__(cls)

        return cls.instance

    def loadLessons(self):
        hasErrors = False

        # TODO: load built-in lessons

        # load lessons from the user directory
        lessonsPath = QgsSettings().value('qtutor/lessonsPath',
                                          os.path.join(QgsApplication.qgisSettingsDirPath(), 'lessons'))

        for groupDir in os.scandir(lessonsPath):
            if groupDir.is_file:
                continue

            for lessonDir in os.scandir(os.path.join(lessonsPath, groupDir)):
                root = os.path.join(lessonsPath, groupDir, lessonDir)
                if utils.isLesson(root):
                    lesson = Lesson.fromYaml(os.path.join(root, 'lesson.yaml'))
                    if lesson:
                        self._addLesson(lesson)
                    else:
                        hasErrors = True

        return hasErrors

    def addLessonsDirectory(self, directory):
        for entry in os.scandir(directory):
            if utils.isLesson(os.path.join(directory, entry.name)):
                lesson = Lesson.fromYaml(os.path.join(directory, entry.name, 'lesson.yaml'))
                if lesson:
                    self._addLesson(lesson)

    def removeLessonsDirectory(self, directory):
        for entry in os.scandir(directory):
            if utils.isLesson(os.path.join(directory, entry.name)):
                lesson = Lesson.fromYaml(os.path.join(directory, entry.name, 'lesson.yaml'))
                if lesson:
                    self._removeLesson(lesson)

    def _addLesson(self, lesson):
        for i in self.lessons:
            if i.id == lesson.id:
                return
        self.lessons.append(lesson)

    def _removeLesson(self, lesson):
        for i in self.lessons:
            if i.id == lesson.id:
                self.lessons.remove(i)
