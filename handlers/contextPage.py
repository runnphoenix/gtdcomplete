#!/usr/bin/python

from .handler import Handler
from models import Context
from . import accessControl


class ContextPage(Handler):
    @accessControl.user_logged_in
    @accessControl.context_exist
    def get(self, context_id, context):

        (finished_events, unfinished_events) = self.eventsInContainer(context)
        self.render("contextPage.html",
            context_name=context.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events)

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

            (finished_events, unfinished_events) = self.eventsInContainer(context)
            self.render("contextPage.html",
                context_name=context.name,
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
