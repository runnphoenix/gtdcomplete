#/usr/bin/python

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from apiclient import discovery
import random
import string
import json
import accessControl
from handler import Handler
from httplib2 import Http
import datetime

from apiclient.discovery import build
from google.appengine.ext import webapp

from oauth2client.contrib.appengine import AppAssertionCredentials
from oauth2client.contrib.appengine import OAuth2Decorator
from google.appengine.api import memcache

decorator = OAuth2Decorator(
  client_id='616429551496-5pq095a8rujmih0l0alfrl8jgadqtaaj.apps.googleusercontent.com',
  client_secret='7kOx9i9yDJriYbJbpFvDaizI',
  scope='https://www.googleapis.com/auth/calendar')
service = discovery.build('calendar', 'v3')

#http://gtdcomplete-171902.appspot.com/oauth2callback?
#state=http://gtdcomplete-171902.appspot.com/calendar:vr_52GqbH7YdFjqhC2V7YjoxNTA2NzU0MzYy&code=4/ZHVTxp_T_eQuxCveoeQERl6Qa7-DafJOP_jEW0NbiAc#

class Calendar(Handler):
	def get(self):
		self.render('calendar.html')

	@decorator.oauth_required
	def post(self):


		http = decorator.http()
		request = service.events().list(calendarId='primary')
		response = request.execute(http=http)
		self.render('calendar.html', response=response)



		#credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/calendar')
		#http_auth = credentials.authorize(Http(memcache))
		#print(http_auth.__dict__)
		#service = discovery.build('calendar', 'v3', http=http_auth)
	#	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	#	eventsResult = service.events().list(
	#		calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
	#		orderBy='startTime').execute()
	#	events = eventsResult.get('items', [])
	#	if not events:
	#		errMessage = 'No Events Found.'
	#	else:
	#		errMessage = 'Events Founded.'
	#	for event in events:
	#		start = event['start'].get('dateTime', event['start'].get('date'))

		#calendar_list_entry = service.calendarList().get(calendarId='calendarId').execute()

		#self.render('calendar.html',calendarlist=calendar_list_entry,errMessage=errMessage,credentials=credentials.__dict__,eventsResult=eventsResult,auth=http_auth,service=service)



	#	print(self.user.state,self.request.get('state'))
	#	if self.request.get('state') != self.user.state:
	#		print("Not same User!")
	#	# one time code
	#	code = self.request.body
	#	try:
	#		# Upgrade the authorization code into a credentials object
	#		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
	#		oauth_flow.redirect_uri = 'postmessage'
	#		credentials = oauth_flow.step2_exchange(code)
	#	except FlowExchangeError:
	#		response = make_response(
	#			json.dumps('Failed to upgrade the authorization code.'), 401)
	#		response.headers['content-Type'] = 'application/json'
	#		return response
	#	# check if the access token is valid.
	#	access_token = credentials.access_token
	#	url = (
	#		'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
	#		access_token)
	#	h = httplib2.Http()
	#	result = json.loads(h.request(url, 'GET')[1])
	#	print(result)
	#	# if there was error in access token info got
	#	if result.get('error') is not None:
	#		response = make_response(json.dumps(result.get('error')), 500)
	#		response.headers['Content-Type'] = 'application/json'
	#	# Verify that the access token is used for the intended user.
	#	gplus_id = credentials.id_token['sub']
	#	if result['user_id'] != gplus_id:
	#		response = make_response(
	#			json.dumps("Token's user ID doesn't match given user ID"), 401)
	#		response.headers['Content-Type'] = 'application/json'
	#		return response
	#	# check if user is already logged in
	#	stored_credentials = login_session.get('credentials')
	#	stored_gplus_id = login_session.get('gplus_id')
	#	if stored_credentials is not None and gplus_id == stored_gplus_id:
	#		response = make_response(
	#			json.dumps('Current user is already connected.'), 200)
	#		response.headers['Content-Type'] = 'application/json'

	#	# store the access token in the session for later use.
	#	login_session['credentials'] = credentials.access_token
	#	login_session['gplus_id'] = gplus_id

	#	# get user info
	#	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	#	params = {'access_token': credentials.access_token, 'alt': 'json'}
	#	answer = requests.get(userinfo_url, params=params)
	#	data = json.loads(answer.text)

	#	login_session['user_name'] = data['name']
	#	login_session['picture'] = data['picture']
	#	login_session['email'] = data['email']

	#	# see if user exists
	#	user_id = getUserID(login_session['email'])
	#	if not user_id:
	#		user_id = createUser(login_session)
	#	login_session['user_id'] = user_id

	#	output = ''
	#	output += '<h1>Welcome, '
	#	output += login_session['user_name']
	#	output += '!</h1>'

	#	output += '<img src="'
	#	output += login_session['picture']
	#	output += '"style = "width: 300px; height: 300px; border-radius:150px;'
	#	output += ' -webkit-border-radius: 150px;-moz-border-radisu: 150px;"> '

	#	flash("you are now logged in as %s" % login_session['user_name'])
	#	return output
