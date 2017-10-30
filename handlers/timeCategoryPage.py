#!/usr/bin/python

from .handler import Handler
from models import TimeCategory
from . import accessControl


class TimeCategoryPage(Handler):

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def get(self, timeCategory_id, timeCategory):
        (finished_events, unfinished_events) = self.eventsInContainer(timeCategory)
        self.render("timeCategoryPage.html",
            timeCategory_name=timeCategory.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events)

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def post(self, timeCategory_id, timeCategory):
        if 'Delete Category' in self.request.params:
            for event in timeCategory.events:
                event.delete()
            timeCategory.delete()
            self.redirect("/timeCategories")
        else: #Update
            category_name = self.request.get('timeCategory_name')
            timeCategory.name = category_name
            timeCategory.put()

            (finished_events, unfinished_events) = self.eventsInContainer(timeCategory)
            self.render("timeCategoryPage.html",
                timeCategory_name=timeCategory.name,
                finished_events=finished_events,
                unfinished_events=unfinished_events)

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
