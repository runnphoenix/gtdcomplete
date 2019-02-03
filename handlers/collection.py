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
        self.render("collection.html", events=self.events_in_project('inbox'))

    @accessControl.user_logged_in
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

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

    def events_in_project(self, project_name):
        for project in self.user.projects:
            if project.name == project_name:
                return project.events
