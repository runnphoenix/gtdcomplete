#!/usr/bin/python

import re
from google.appengine.ext import db
from handler import Handler
from models import User


def users_key(group='default'):
    return db.Key.from_path("users", group)


class Signup(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        self.userName = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        has_error = False
        params = dict(username=self.userName, email=self.email)

        if not self.username_valid(self.userName):
            params['error_username'] = "Not a valid user name."
            has_error = True

        if not self.password_valid(self.password):
            params['error_password'] = "Not a valid password."
            has_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Passwords don't match."
            has_error = True

        if self.email and (not self.email_valid(self.email)):
            params['error_email'] = "Not a valid email."
            has_error = True

        if has_error:
            self.render("signup.html", **params)
        else:
            self.finish()

    # Judge username etc
    def username_valid(self, name):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(name)

    def password_valid(self, password):
        PSWD_RE = re.compile(r"^.{3,20}$")
        return PSWD_RE.match(password)

    def email_valid(self, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return EMAIL_RE.match(email)

    def finish(self):
        user = User.by_name(self.userName)
        if user:
            errorMessage = "User already exist."
            self.render("signup.html", error_username=errorMessage)
        else:
            pw_hash = User.make_pw_hash(self.userName, self.password)
            user = User(
                parent=users_key(),
                name=self.userName,
                pw_hash=pw_hash,
                email=self.email)
            user.put()
            # set cookie
            self.add_cookie(user)
            # redirect
            self.redirect('/welcome')
