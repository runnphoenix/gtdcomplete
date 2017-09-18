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
        startYear = startDate.year
        endYear = endDate.year
        startMonth = startDate.month
        endMonth = endDate.month
        errMessage = ''
        if startDate > endDate:
            errMessage = "End date MUST be bigger than start date."
        else: # with duration
            days = (endDate - startDate).days + 1

        # get all events
        result = {}
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                if event.time_exe_start.date() >= startDate.date() and event.time_exe_end.date() <= endDate.date():
                    categoryTime = categoryTime + (event.time_exe_end - event.time_exe_start).seconds / 60
            result[timeCategory.name] = [categoryTime, float(categoryTime)/24/60/days*100]

        self.render("statistics.html",
                    startDate=startDate,
                    endDate=endDate,
                    result=result,
                    errMessage = errMessage)
