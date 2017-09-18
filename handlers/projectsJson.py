#!/usr/bin/python

import accessControl
from handler import Handler
import json

class ProjectsJson(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        projects = []
        for project in self.user.projects:
            projects.append(project.name)
        obj = {
            'projects': projects
        }
        self.response.out.write(json.dumps(obj))
