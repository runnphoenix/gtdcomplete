#!/usr/bin/python

from google.appengine.ext import db
from .user import User


class Context(db.Model):
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, collection_name='contexts')
