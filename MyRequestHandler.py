import app
import tornado.web

class MyRequestHandler(tornado.web.RequestHandler):
	def initialize(self, config, state):
		self.config = config
		self.state = state

	@tornado.web.asynchronous
	def get(self):
		"""POST handler"""

	@tornado.web.asynchronous
	def post(self):
		"""POST handler"""
		post_data = self.request.body

		try:
			reply = app.do(post_data)
			self.write(reply)
			self.finish()
		except:
			self.send_error(500)
