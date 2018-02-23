#/usr/bin/python

from . import accessControl
from .handler import Handler


class UnfinishedEvents(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("unfinishedEvents.html", events=self.unfinishedEvents())

    def unfinishedEvents(self):
        unfinishedEvents = []
        for project in self.user.projects:
            print project.name
            events = project.events
            if events is not None:
                for event in events:
                    print event.title
                    if event.finished == False:
                        unfinishedEvents.append(event)
        return unfinishedEvents

    @accessControl.user_logged_in
    def post(self):
        pass
