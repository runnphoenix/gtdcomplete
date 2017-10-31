#!/usr/bin/python

from .handler import Handler
from models import Project
from . import accessControl
from datetime import datetime,timedelta
import pytz

class ProjectPage(Handler):

    @accessControl.user_logged_in
    @accessControl.project_exist
    def get(self, project_id, project):
        (finished_events, unfinished_events) = self.eventsInContainer(project)
        self.render("projectPage.html",
            project_name=project.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            xxx=self.request.params)


    @accessControl.user_logged_in
    @accessControl.project_exist
    def post(self, project_id, project):

        self.render("projectPage.html",
            project_name=project.name,
            finished_events=[],
            unfinished_events=[],
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            xxx=self.request.params)
