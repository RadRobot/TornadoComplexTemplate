import tornado.ioloop
from tornado.httpserver import HTTPServer
import tornado.web
from tornado.netutil import bind_sockets
from tornado.process import fork_processes, task_id

# configuration
import config
from pigeon.pigeon import PConf

# app specific libraries
from state import AppState
from MyRequestHandler import MyRequestHandler

if __name__ == "__main__":

	config = PConf("system.config", config.schema)

	# state can store objects that get updated asyncronously and are needed everywhere
	shared_system_state = AppState(config)

	# multiple request handlers, sharing the same state
	tornado_app_config = tornado.web.Application([
			( r"/some_path", MyRequestHandler, dict(config=config, state=shared_system_state) ),
		])

	# listen on the configured port, default to 8888 if not specified
	sockets = bind_sockets(config.get('port', 8888))

	# multi-process tornado. auto forks for every core you have
	fork_processes()

	# grab the task id so you can use it to refer to unique sub processes
	shared_system_state.task_id = task_id()

	# set the server's application handler
	server = HTTPServer(tornado_app_config)
	server.add_sockets(sockets)

	# create the io loop
	main_loop = tornado.ioloop.IOLoop.instance()	

	# can add multiple asyncronous periodic loops
	async_loop = tornado.ioloop.PeriodicCallback( shared_system_state.async_function,
							config.conf['async_loop_period'],
							io_loop=main_loop )

	async_loop.start()
	main_loop.start()
