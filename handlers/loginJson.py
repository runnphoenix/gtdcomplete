#!/usr/bin/python

from .signup import Signup
from models import User
import json
import hmac

class LoginJson(Signup):

    def post(self):
        requestString = self.request.body
        request = json.loads(requestString)
        username = request['username']
        password = request['password']

        has_error = False
        params = dict(username=username, password=password)

        if not self.username_valid(username):
            params['error_username'] = "Not a valid user name."
            has_error = True

        if not self.password_valid(password):
            params['error_password'] = "Not a valid password."
            has_error = True

        if has_error:
            self.response.out.write(json.dumps(params))
        else:
            user = User.by_name(username)
            if user:
                if User.valid_hash(username, password, user.pw_hash):
                    user_id = str(user.key().id())
                    secure_id = make_secure_val(user_id)
                    self.write(json.dumps(dict(uid=secure_id)))
                    #self.redirect('/projects')
                else:
                    params['passwd_unmatch'] = "Password unmatch"
                    self.response.out.write(json.dumps(params))
            else:
                params['user_noexist'] = "User not exist"
                self.response.out.write(json.dumps(request))


secret = 'BurningPyre'
def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())
