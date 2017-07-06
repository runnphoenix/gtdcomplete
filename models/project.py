#!/usr/bin/python

from google.appengine.ext import db
from user import User

class Project(db.Model):
	name = db.StringProperty(required=True)
	user = db.ReferenceProperty(User, collection_name='projects')
