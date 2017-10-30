#!/usr/bin/python

from .handler import Handler
from models import TimeCategory
from . import accessControl


class TimeCategoryPage(Handler):
    finished_events = {}
    unfinished_events = {}

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def get(self, timeCategory_id, timeCategory):

        for event in timeCategory.events:
            if event.finished:
                if not self.finished_events.get(str(event.time_exe_start.date())):
                    self.finished_events[str(event.time_exe_start.date())] = [event]
                else:
                    self.finished_events[str(event.time_exe_start.date())].append(event)
            else:
                if not self.unfinished_events.get(str(event.time_exe_start.date())):
                    self.unfinished_events[str(event.time_exe_start.date())] = [event]
                else:
                    self.unfinished_events[str(event.time_exe_start.date())].append(event)
        self.render("timeCategoryPage.html",
            timeCategory_name=timeCategory.name,
            finished_events=self.finished_events,
            unfinished_events=self.unfinished_events)

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
            self.render("timeCategoryPage.html",
                timeCategory_name=timeCategory.name,
                finished_events=self.finished_events,
                unfinished_events=self.unfinished_events)
