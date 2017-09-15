#!/usr/bin/python

from handler import Handler
from models import Project
from models import TimeCategory
from models import Event
import accessControl

from datetime import datetime, date, time
from google.appengine.ext import db

class YearStatistics(Handler):

    @accessControl.user_logged_in
    def get(self):
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                if event.time_exe_start.year == date.today().year:
                    categoryTime = categoryTime + (event.time_exe_end - event.time_exe_start).seconds / 60
            # Need to calculate how many days
            result[timeCategory.name] = [categoryTime, float(categoryTime)/24/0.6/self.dayNumberYear(date.today().year)]
        self.render("statistics.html", result=result)

    def dayNumberYear(self, year):
        if year % 4 == 0:
            return 366
        else:
            return 365
