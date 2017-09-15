#!/usr/bin/python

from handler import Handler
from models import Project
from models import TimeCategory
from models import Event
import accessControl

from datetime import datetime, date, time
from google.appengine.ext import db

class MonthStatistics(Handler):

    @accessControl.user_logged_in
    def get(self):
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                if event.time_exe_start.month == date.today().month:
                    categoryTime = categoryTime + (event.time_exe_end - event.time_exe_start).seconds / 60
            # Need to calculate how many days
            result[timeCategory.name] = [categoryTime, float(categoryTime)/24/0.6/self.dayNumbers(date.today().year, date.today().month)]
        self.render("statistics.html", result=result)


    def dayNumbers(self, year, month):
        longerMonths = [1,3,5,7,8,10,12]
        shorterMonths = [4,6,9,11]
        if month in longerMonths:
            return 31
        elif month in shorterMonths:
            return 30
        else:
            if year % 4 == 0:
                return 29
            else:
                return 28
