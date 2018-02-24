#!/usr/bin/python

from .signup import Signup
from models import User
import json

class LoginJson(Signup):

    def post(self):
        requestString = self.request.body
        request = json.loads(requestString)
        print(request)

        #user = User.by_name()
        self.response.out.write(json.dumps(request))
