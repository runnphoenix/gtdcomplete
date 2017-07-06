#!/usr/bin/python

from signup import Signup
from models import User


class Login(Signup):

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        has_error = False
        params = dict(username=username, password=password)

        if not self.username_valid(username):
            params['error_username'] = "Not a valid user name."
            has_error = True
            print(params)

        if not self.password_valid(password):
            params['error_password'] = "Not a valid password."
            has_error = True

        if has_error:
            self.render("login.html", **params)
        else:
            user = User.by_name(username)
            if user:
                if User.valid_hash(username, password, user.pw_hash):
                    self.add_cookie(user)
                    self.redirect('/welcome')
                else:
                    self.render(
                        "login.html",
                        username=username,
                        error_password_wrong="Wrong passowrd.")
            else:
                self.render(
                    "login.html",
                    error_user_exist="No such user, please signup first.")
