
"""
	This is a shareable object.
	The state can be mutated by multiple request handlers.
	A good place for database connections, message queues, periodic data, etc

"""

import deta
import localog

class AppState:
	def __init__(self, config):
		self.dbg = deta()
		self.logger = localog()

		# you can either put app specific things in here directly,
		# or extend this generic state object and create an app specific state,
		# then extend the specific state object when you create the app class
		# OR
		# extend this generic object with the app class and store things directly in there
		# but if the state is complex enough, I recommend keeping the state separate from the app!
