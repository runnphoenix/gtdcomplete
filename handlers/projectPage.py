#!/usr/bin/python

from .handler import Handler
from models import Project
from . import accessControl


class ProjectPage(Handler):

    @accessControl.user_logged_in
    @accessControl.project_exist
    def get(self, project_id, project):
        finished_events = {}
        unfinished_events = {}
        for event in project.events:
            if event.finished:
                if not finished_events.get(str(event.time_exe_start.date())):
                    finished_events[str(event.time_exe_start.date())] = [event]
                else:
                    finished_events[str(event.time_exe_start.date())].append(event)
            else:
                if not unfinished_events.get(str(event.time_plan_start.date())):
                    unfinished_events[str(event.time_plan_start.date())] = [event]
                else:
                    unfinished_events[str(event.time_plan_start.date())].append(event)
        self.render("projectPage.html",
            project_name=project.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events)
                
    @accessControl.user_logged_in
    @accessControl.project_exist
    def post(self, project_id, project):
        for event in project.events:
            event.delete()
        project.delete()
        self.redirect("/projects")
