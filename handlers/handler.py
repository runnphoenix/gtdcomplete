#!/usr/bin/python

import hmac
import os
import webapp2
import jinja2
from models import User

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(template_dir),
	autoescape=True)

secret = 'BurningPyre'

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

def make_secure_val(val):
	return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(h):
	val = h.split('|')[0]
	if make_secure_val(val) == h:
		return val

class Handler(webapp2.RequestHandler):
	
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render(self, template, **kw):
		kw['logged'] = self.user
		self.write(render_str(template, **Kw))

	def add_cookie(self, user):
		user_id = str(user.key().id())
		secure_id = make_secure_val(user_id)
		self.response.headers.add_header(
			'Set-Cookie', 'user_id=%s; Path=/' % secure_id)

	def read_cookies(self):
		cookie_val = self.request.cookies.get('user_id')
		return cookie_val and check_secure_val(cookie_val)

	def reset_cookie(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initilize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_cookie()
		self.user = uid and User.by_id(int(uid))
