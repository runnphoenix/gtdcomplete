#!/usr/bin/python

import accessControl
from handler import Handler
import json

class ProjectsJson(Handler):

    @accessControl.user_logged_in
    def get(self):
        print {'projects':[x.name for x in self.user.projects]}
        return json.dumps({'projects':[x.name for x in self.user.projects]})
