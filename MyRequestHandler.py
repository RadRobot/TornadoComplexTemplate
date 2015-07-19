import app_core
import tornado.web

class MyRequestHandler(tornado.web.RequestHandler):
	def initialize(self, config, app_state):
		self.config = config
		self.app_state = app_state

	@tornado.web.asynchronous
	def get(self):
		"""GET handler"""

		self.write()
		self.finish()

	@tornado.web.asynchronous
	def post(self):
		"""POST handler"""
		post_data = self.request.body

		try:
			reply = app_core.do(post_data, self.app_state)

			self.write(reply)
			self.finish()
		except:
			self.send_error(500)
