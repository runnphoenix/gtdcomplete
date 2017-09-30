#!/usr/bin/python

import random
import hashlib
from string import letters
from google.appengine.ext import db

def users_key(group='default'):
	return db.Key.from_path("users", group)

class User(db.Model):
	name = db.StringProperty(required=True)
	pw_hash = db.StringProperty(required=True)
	email = db.StringProperty()

	@classmethod
	def by_name(cls, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def by_id(cls, user_id):
		return User.get_by_id(user_id, parent=users_key())

	@classmethod
	def signup(cls, username, pw, email=None):
		pw_hash = User.make_pw_hash(username, pw)
		user = User(name=username, pw_hash=pw_hash, email=email)

	@classmethod
	def make_salt(cls, length=5):
		return ''.join(random.choice(letters) for x in xrange(length))

	@classmethod
	def make_pw_hash(cls, name, pw, salt=None):
		if not salt:
			salt = User.make_salt()
		h = hashlib.sha256(name+pw+salt).hexdigest()
		return "%s,%s" % (salt, h)

	@classmethod
	def valid_hash(cls, name, pw, h):
		salt = h.split(',')[0]
		return h == User.make_pw_hash(name, pw, salt)
