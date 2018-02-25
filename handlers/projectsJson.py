#!/usr/bin/python

from . import accessControl
from .handler import Handler
import json


class ProjectsJson(Handler):

    @accessControl.user_logged_in
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        projects = {}
        for project in self.user.projects:
            projects[project.key().id()] = project.name
        self.response.out.write(json.dumps(projects))
