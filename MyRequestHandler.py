import tornado.web

class MyRequestHandler(tornado.web.RequestHandler):
	def initialize(self, config, app):
		self.config = config
		self.app = app

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
			reply = self.app.do(post_data, self.app_state)

			self.write(reply)
			self.finish()
		except:
			self.send_error(500)

	@tornado.web.asynchronous
	def head(self):
		"""HEAD handler"""

		self.write("app info")
		self.finish()

	@tornado.web.asynchronous
	def ping(self):
		"""PING handler"""

		self.send_error(200)
