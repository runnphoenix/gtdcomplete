#!/usr/bin/python

from .handler import Handler
from models import Context
from . import accessControl
from datetime import datetime, timedelta
import pytz

shanghai = pytz.timezone('Asia/Shanghai')
rome = pytz.timezone('Europe/Rome')

class ContextPage(Handler):
    @accessControl.user_logged_in
    @accessControl.context_exist
    def get(self, context_id, context):
        (finished_events, unfinished_events) = self.eventsInContainer(context)
        self.render("contextPage.html",
            contexts=self.user.contexts,
            context_name=context.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(rome),
            endDate=datetime.now(rome)

    @accessControl.user_logged_in
    @accessControl.context_exist
    def post(self, context_id, context):
        if 'Delete' in self.request.params:
            for event in context.events:
                event.delete()
            context.delete()
            self.redirect("/contexts")
        elif "Update" in self.request.params:
            context_name = self.request.get('context_name')
            context.name = context_name
            context.put()
            (finished_events, unfinished_events) = self.eventsInContainer(context)
            self.render("contextPage.html",
                contexts=self.user.contexts,
                context_name=context.name,
                finished_events=finished_events,
                unfinished_events=unfinished_events,
                startDate=datetime.now(rome),
                endDate=datetime.now(rome))
        else: #Look up finished events
            startDate = datetime.strptime(self.request.get("startDate"),"%Y-%m-%d")
            endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
            if startDate > endDate:
                errMessage = "End date MUST be bigger than start date."
                self.render("contextPage.html",
                    contexts=self.user.contexts,
                    context_name=context.name,
                    finished_events=[],
                    unfinished_events=[],
                    startDate=datetime.now(rome),
                    endDate=datetime.now(rome),
                    errMessage=errMessage)
            else:  # with duration
                days = (endDate - startDate).days + 1
                dates = [(startDate + timedelta(i)).date() for i in range(days)]
                (finished_events, unfinished_events) = self.eventsInContainer(context, dates)
                self.render("contextPage.html",
                    contexts=self.user.contexts,
                    context_name=context.name,
                    finished_events=finished_events,
                    unfinished_events=unfinished_events,
                    startDate=datetime.now(rome),
                    endDate=datetime.now(rome))

    def eventsInContainer(self, container, lookupDates=[]):
        finished_events = {}
        unfinished_events = {}
        for event in container.events:
            if event.finished:
                if event.time_exe_start.date() in lookupDates:
                    if not finished_events.get(str(event.time_exe_start.date())):
                        finished_events[str(event.time_exe_start.date())] = [event]
                    else:
                        finished_events[str(event.time_exe_start.date())].append(event)
            else:
                if event.time_plan_start:
                    if not unfinished_events.get(str(event.time_plan_start.date())):
                        unfinished_events[str(event.time_plan_start.date())] = [event]
                    else:
                        unfinished_events[str(event.time_plan_start.date())].append(event)
        return (finished_events, unfinished_events)
