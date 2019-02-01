#/usr/bin/python

from . import accessControl
from .handler import Handler

from datetime import datetime, timedelta
import pytz

class TimeCategoriesW(Handler):

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def get(self, timeCategory_id, timeCategory):
        timeCategories=self.user.timeCategories
        (finished_events, unfinished_events) = self.eventsInContainer(timeCategory)
        self.render(
            "timeCategoriesW.html",
            timeCategories=timeCategories,
            timeCategory_name=timeCategory.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')))

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def post(self):
        pass

    def eventsInContainer(self, container, lookupDates=[]):
        finished_events = {}
        unfinished_events = {}
        for event in container.events:
            if event.finished:
                if event.time_exe_start.date() in lookupDates:
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
