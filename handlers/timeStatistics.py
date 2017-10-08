#!/usr/bin/python

from .handler import Handler
from models import Project
from models import TimeCategory
from models import Event
from . import accessControl

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
        startDate = datetime.strptime(
            self.request.get("startDate"),
            "%Y-%m-%d")
        endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
        # claculate days count
        startYear = startDate.year
        endYear = endDate.year
        startMonth = startDate.month
        endMonth = endDate.month
        errMessage = ''
        if startDate > endDate:
            errMessage = "End date MUST be bigger than start date."
        else:  # with duration
            days = (endDate - startDate).days + 1

        # get all events
        result = {}
        recordedTimeCount = 0
        timeCategories = self.user.timeCategories
        for timeCategory in timeCategories:
            categoryTime = 0
            for event in timeCategory.events:
                eventStartT = event.time_exe_start
                eventEndT = event.time_exe_end
                # Event across Midnight: 0.whole event in 1.first half in
                # 2.second half in
                if eventStartT.date() >= startDate.date() and eventEndT.date() <= endDate.date():
                    categoryTime = categoryTime + \
                        (eventEndT - eventStartT).seconds / 60
                elif eventStartT.date() == startDate.date() and (eventEndT.date() - endDate.date()).days == 1:
                    categoryTime = categoryTime + \
                        (23 - eventStartT.hour) * 60 + 60 - eventStartT.minute
                elif (startDate.date() - eventStartT.date()).days == 1 and eventEndT.date() == endDate.date():
                    categoryTime = categoryTime + \
                        eventEndT.hour * 60 + eventEndT.minute
            if categoryTime > 0:
                result[timeCategory.name] = [
                    categoryTime, float(categoryTime) / 24 / 60 / days * 100]
            # For time that not recorded
            recordedTimeCount = recordedTimeCount + categoryTime
        recordedTime = [
            recordedTimeCount,
            float(
                recordedTimeCount) /
            24 /
            60 /
            days *
            100]

        self.render("statistics.html",
                    startDate=startDate,
                    endDate=endDate,
                    result=result,
                    recordedTime=recordedTime,
                    errMessage=errMessage)
