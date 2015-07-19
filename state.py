
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

