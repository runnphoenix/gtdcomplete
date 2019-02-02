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
            if event.project == None:
                print(event.key().id())
                events.append(event)
        self.render("collection.html", events=events)

    @accessControl.user_logged_in
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        errorMessage = self.erMessage(title)
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
                parent=events_key()
            )
            event.put()
            self.redirect("/collection")


    def erMessage(self, title):
        if not title:
            return "Field is Empty."
        elif ' ' in title:
            return "No space allowed in title."
        else:
            return None
