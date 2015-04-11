import tornado.web
from tornado.escape import json_encode
from spark import spark
import threading

commands = []
def spark_poll_loop():
  global commands
  commands = spark.get_commands()
  threading.Timer(0.25, spark_poll_loop).start()
spark_poll_loop()

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello')

class CommandHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(json_encode(commands))

application = tornado.web.Application([
  (r"/", MainHandler),
  (r"/what-should-i-do", CommandHandler),
])
