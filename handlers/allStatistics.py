#!/usr/bin/python

from handler import Handler
from models import Project
from models import TimeCategory
from models import Event
import accessControl

from datetime import datetime, date, time
from google.appengine.ext import db

class AllStatistics(Handler):

    @accessControl.user_logged_in
    def get(self):
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                categoryTime = categoryTime + (event.time_exe_end - event.time_exe_start).seconds / 60
            # Need to calculate how many days
            result[timeCategory.name] = [categoryTime, float(categoryTime)/24/0.6]
        self.render("statistics.html", result=result)
