#/usr/bin/python

from . import accessControl
from .handler import Handler
from models import Event
from google.appengine.ext import db

def events_key(name="default"):
    return db.Key.from_path("events", name)

class Collection(Handler):
    @accessControl.user_logged_in
    def get(self):
        events = []
        for event in self.user.events:
            if event.project.name == 'inbox':
                events.append(event)
        self.render("collection.html", events=events)

    @accessControl.user_logged_in
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if errorMessage:
            self.render("collection.html",
                eventTitle=title,
                eventContent=content,
                finished=False,
                errorMessage=errorMessage)
        else:
            event = Event(
                title=title,
                content=content,
                finished=False,
                user=self.user,
                project=self.get_inbox_project(),
                parent=events_key()
            )
            event.put()
            self.redirect("/collection")

    def get_inbox_project(self):
        pro = None
        for project in self.user.projects:
            if project.name == 'inbox':
                pro = project
        return pro
