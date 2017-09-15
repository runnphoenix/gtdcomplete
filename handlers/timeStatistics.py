#!/usr/bin/python

from handler import Handler
from models import Project
from models import TimeCategory
from models import Event
import accessControl

from datetime import datetime, date, time
from google.appengine.ext import db

import pytz

class TimeStatistics(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("statistics.html",
                    startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    endDate=datetime.now(pytz.timezone('Asia/Shanghai'))
                    )

    @accessControl.user_logged_in
    def post(self):
        startDate = datetime.strptime(self.request.get("startDate"), "%Y-%m-%d")
        endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
        # claculate days count


        # get all events
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                if event.time_exe_start.date() > startDate and event.time_exe_end < endDate:
                    categoryTime = categoryTime + (event.time_exe_end - event.time_exe_start).seconds / 60
            # Need to calculate how many days
            result[timeCategory.name] = [categoryTime, float(categoryTime)/24/0.6/days]

        self.render("statistics.html",
                    startDate=startDate,
                    endDate=endDate,
                    result=result
                    )

    def dayNumbersMonth(self, year, month):
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
