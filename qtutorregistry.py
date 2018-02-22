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
import shutil
import zipfile

from qgis.core import QgsApplication, QgsSettings

from qtutor.lesson import Lesson
from qtutor import utils

pluginPath = os.path.dirname(__file__)


class QTutorRegistry:

    def __init__(self):
        self.groups = dict()
        self.lessons = dict()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(QTutorRegistry, cls).__new__(cls)

        return cls.instance

    def loadLessons(self):
        # load built-in lessons
        skipBuiltin = QgsSettings().value('qtutor/skipBuiltin', False, bool)
        if not skipBuiltin:
            self._loadFromDirectory(os.path.join(pluginPath, 'lessons'))

        # load lessons from the user directories
        pathsList = QgsSettings().value('qtutor/lessonsPaths',
                                [os.path.join(QgsApplication.qgisSettingsDirPath(), 'lessons')])
        for directory in pathsList:
            if os.path.exists(directory):
                for entry in os.scandir(directory):
                    if entry.is_file:
                        continue

                    self._loadFromDirectory(os.path.join(directory, entry.name))

    def addLessonsDirectory(self, directory):
        self._loadFromDirectory(directory)

    def removeLessonsDirectory(self, directory):
        for entry in os.scandir(directory):
            if utils.isLesson(os.path.join(directory, entry.name)):
                lessonId = Lesson.idFromYaml(os.path.join(directory, entry.name, 'lesson.yaml'))
                if lessonId:
                    self._removeLesson(lessonId)

    def lessonById(self, lessonId):
        group, name = lessonId.split(':')

        if group in self.lessons and lessonId in self.lessons[group]:
            return self.lessons[group][lessonId]

        return None

    def installLessonsFromZip(self, filePath):
        # TODO: allow multiple groups inside archive
        pathsList = QgsSettings().value('qtutor/lessonsPaths',
                                        [os.path.join(QgsApplication.qgisSettingsDirPath(), 'lessons')])

        with zipfile.ZipFile(filePath, 'r') as zf:
            zf.extractall(pathsList[0])

        dirName = os.path.splitext(filePath)[0]
        self._loadFromDirectory(os.path.join(pathsList[0], dirName))
        return True

    def uninstallLesson(self, lessonId):
        lesson = self.lessonById(lessonId)
        if lesson:
            lessonsPath = QgsSettings().value('qtutor/lessonsPath',
                                              os.path.join(QgsApplication.qgisSettingsDirPath(), 'lessons'), str)
            # only user lessons can be uninstalled
            if not lesson.root.startswith(lessonsPath):
                QgsMessageLog.logMessage(self.tr('Lesson "{}" is not a user lesson and can not be uninstalled.'.format(lesson.name)))
                return False

            rootDirectory = lesson.root
            self._removeLesson(lesson)
            shutil.rmtree(rootDirectory)
            return True

    def _loadFromDirectory(self, directory):
        for lessonDir in os.scandir(directory):
            root = os.path.join(directory, lessonDir.name)
            if utils.isLesson(root):
                lesson = Lesson.fromYaml(os.path.join(root, 'lesson.yaml'))
                if lesson:
                    self._addLesson(lesson)

    def _addLesson(self, lesson):
        groupId = lesson.groupId
        if groupId not in self.groups:
            self.groups[groupId] = lesson.group
            self.lessons[groupId] = {}

        if lesson.name in self.lessons[groupId]:
            QgsMessageLog.logMessage(self.tr('Duplicate lesson name "{}" for group "{}"'.format(lesson.name, groupId)))
            return

        self.lessons[groupId][lesson.id] = lesson

    def _removeLesson(self, lessonId):
        groupId, name = lessonId.split(":")
        if groupId not in self.groups:
            return

        if name in self.lessons[groupId]:
            del self.lessons[groupId][name]
            if len(self.lessons[groupId]) == 0:
                del self.lessons[groupId]
                del self.groups[groupId]

    def tr(self, text):
        return QCoreApplication.translate('QTutorRegistry', text)
