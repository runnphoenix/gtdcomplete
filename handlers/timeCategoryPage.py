#!/usr/bin/python

from .handler import Handler
from models import TimeCategory
from . import accessControl
from datetime import datetime
import pytz


class TimeCategoryPage(Handler):

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def get(self, timeCategory_id, timeCategory):
        (finished_events, unfinished_events) = self.eventsInContainer(timeCategory)
        self.render("timeCategoryPage.html",
            timeCategory_name=timeCategory.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')))

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def post(self, timeCategory_id, timeCategory):
        if 'Delete Category' in self.request.params:
            for event in timeCategory.events:
                event.delete()
            timeCategory.delete()
            self.redirect("/timeCategories")
        elif "Update" in self.request.params:
            timeCategory_name = self.request.get('timeCategory_name')
            timeCategory.name = timeCategory_name
            timeCategory.put()
            (finished_events, unfinished_events) = self.eventsInContainer(timeCategory)
            self.render("timeCategoryPage.html",
                timeCategory_name=timeCategory.name,
                finished_events=finished_events,
                unfinished_events=unfinished_events,
                startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                endDate=datetime.now(pytz.timezone('Asia/Shanghai')))
        else: #Look up finished events
            startDate = datetime.strptime(self.request.get("startDate"),"%Y-%m-%d")
            endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
            if startDate > endDate:
                errMessage = "End date MUST be bigger than start date."
                self.render("timeCategoryPage.html",
                    timeCategory_name=timeCategory.name,
                    finished_events=[],
                    unfinished_events=[],
                    startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    endDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    errMessage=errMessage)
            else:  # with duration
                days = (endDate - startDate).days + 1
                dates = [(startDate + timedelta(i)).date() for i in range(days)]
                (finished_events, unfinished_events) = self.eventsInContainer(timeCategory, dates)
                self.render("timeCategoryPage.html",
                    timeCategory_name=timeCategory.name,
                    finished_events=finished_events,
                    unfinished_events=unfinished_events,
                    startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    endDate=datetime.now(pytz.timezone('Asia/Shanghai')))

    def eventsInContainer(self, container):
        finished_events = {}
        unfinished_events = {}
        for event in container.events:
            if event.finished:
                if not finished_events.get(str(event.time_exe_start.date())):
                    finished_events[str(event.time_exe_start.date())] = [event]
                else:
                    finished_events[str(event.time_exe_start.date())].append(event)
            else:
                if not unfinished_events.get(str(event.time_exe_start.date())):
                    unfinished_events[str(event.time_exe_start.date())] = [event]
                else:
                    unfinished_events[str(event.time_exe_start.date())].append(event)
        return (finished_events, unfinished_events)
