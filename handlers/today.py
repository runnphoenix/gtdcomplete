#/usr/bin/python

from . import accessControl
from .handler import Handler
from datetime import date

class Today(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("today.html", events=self.events_today())

    def events_today(self):
        events_today = {}
        events_today['finished'] = []
        events_today['unfinished'] = []
        today = date.today()
        for project in self.user.projects:
            events = project.events
            if events is not None:
                for event in events:
                    if event.time_plan_start.date() == today or event.time_exe_end.date() == today:
                        if event.finished == True:
                            events_today['finished'].append(event)
                        else:
                            events_today['unfinished'].append(event)
        return events_today

    @accessControl.user_logged_in
    def post(self):
        pass
