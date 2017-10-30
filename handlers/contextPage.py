#!/usr/bin/python

from .handler import Handler
from models import Context
from . import accessControl


class ContextPage(Handler):
    finished_events = {}
    unfinished_events = {}

    @accessControl.user_logged_in
    @accessControl.context_exist
    def get(self, context_id, context):

        for event in context.events:
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
        self.render("contextPage.html",
            context_name=context.name,
            finished_events=self.finished_events,
            unfinished_events=self.unfinished_events)

    @accessControl.user_logged_in
    @accessControl.context_exist
    def post(self, context_id, context):
        if 'Delete Context' in self.request.params:
            for event in context.events:
                event.delete()
            context.delete()
            self.redirect("/contexts")
        else: #Update
            context_name = self.request.get('context_name')
            context.name = context_name
            context.put()
            self.render("contextPage.html",
                context_name=context.name,
                finished_events=self.finished_events,
                unfinished_events=self.unfinished_events)
