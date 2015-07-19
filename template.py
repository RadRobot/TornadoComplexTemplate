import tornado.ioloop
from tornado.httpserver import HTTPServer
import tornado.web
from tornado.netutil import bind_sockets
from tornado.process import fork_processes, task_id

from pigeon.pigeon import PConf
from MyRequestHandler import MyRequestHandler
import SystemState

# store state for all handlers
import queue
class AppState:
	def __init__(self):
		self.queue = queue.Queue()
		self.status = 0
		# etc ...

# see pigeon repo: git@github.com:RadRobot/pigeon.git
config_schema = {
	"port": int,
	"async_loop_period": int
}

if __name__ == "__main__":

	config =  PConf("system.config", config_schema)

	# state can store objects that get updated asyncronously and are needed everywhere
	shared_system_state = SystemState(config)

	# multiple request handlers, sharing the same state
	app = tornado.web.Application([
			( r"/some_path", MyRequestHandler, dict(config=config, state=shared_system_state) ),
			#( r"/other_path", MyOtherRequestHandler, dict(config=config, state=shared_system_state))
		])

	sockets = bind_sockets(config.conf['port'])

	# multi-process tornado. auto forks for every core you have
	fork_processes()

	# grab the task id so you can use it to refer to unique sub processes
	shared_system_state.task_id = task_id()

	# set the server's application handler
	server = HTTPServer(getApplication())
	server.add_sockets(sockets)

	# create the io loop
	main_loop = tornado.ioloop.IOLoop.instance()	

	# can add multiple asyncronous periodic loops
	async_loop = tornado.ioloop.PeriodicCallback( shared_system_state.async_function,
							config.conf['async_loop_period'],
							io_loop=main_loop )

	async_loop.start()
	main_loop.start()
