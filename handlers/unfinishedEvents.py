#/usr/bin/python

from . import accessControl
from .handler import Handler


class UnfinishedEvents(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("unfinishedEvents.html", events=self.unfinishedEvents())

    def unfinishedEvents(self):
        unfinishedEvents = {}
        unfinishedEvents['notScheduled'] = []
        for project in self.user.projects:
            events = project.events
            if events is not None:
                for event in events:
                    if event.finished == False:
                        if not event.time_plan_start:
                            unfinishedEvents['notScheduled'].append(event)
                        else:
                            if not unfinishedEvents.get(str(event.time_plan_start.date())):
                                unfinishedEvents[str(event.time_plan_start.date())] = [event]
                            else:
                                unfinishedEvents[str(event.time_plan_start.date())].append(event)
        return unfinishedEvents

    @accessControl.user_logged_in
    def post(self):
        pass
