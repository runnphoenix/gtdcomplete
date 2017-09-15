#!/usr/bin/python

from handler import Handler
from models import Project
from models import TimeCategory
from models import Event

import accessControl

from datetime import datetime, date, time
from google.appengine.ext import db

class DayStatistics(Handler):
    @accessControl.user_logged_in
    def get(self):
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            print timeCategory.name
            categoryTime = 0
            categoryEvents = timeCategory.events
            for event in categoryEvents:
                # Add time
                print event.title
                print (event.time_exe_end - event.time_exe_start).seconds / 60
        self.render("dayStatistics.html", result=result)
