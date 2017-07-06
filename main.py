
import webapp2

from models import User
from models import Event

from handlers import Signup
from handlers import Login
from handlers import Logout
from handlers import Welcome
#from handlers import NewEvent
#from handlers import EditEvent
#from handlers import DeleteEvent
#from handlers import EventPage
#from handlers import Events
from handlers import MainPage


app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/signup', Signup),
	('/welcome', Welcome),
	('/login', Login),
	('/logout', Logout)
], debug=True)
