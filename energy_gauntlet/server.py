import os
import tornado.web
import tornado.websocket
from tornado.escape import json_encode
from spark import spark
import threading
import config

commands = []
def spark_poll_loop():
  global commands
  commands = spark.get_commands()
  threading.Timer(0.5, spark_poll_loop).start()
spark_poll_loop()

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    with open (os.path.dirname(os.path.realpath(__file__)) + '/../static/index.html', "r") as indexFile:
      self.write(indexFile.read())

class CommandHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'application/json')
    self.write(json_encode(commands))

class RawHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'application/json')
    self.write(json_encode(spark.get_raw()))

class SocketHandler(tornado.websocket.WebSocketHandler):

  def open(self):
    RawSocketHandler.clients.add(self)

  def on_close(self):
    RawSocketHandler.clients.remove(self)

class RawSocketHandler(SocketHandler):
  clients = set()

  @classmethod
  def send_raw(cls, data):
    for clients in cls.clients:
      try:
          clients.write_message(data)
      except:
        pass

class CommandsSocketHandler(SocketHandler):
  clients = set()

  @classmethod
  def send_commands(cls, data):
    for clients in cls.clients:
      try:
          clients.write_message(data)
      except:
        pass

spark.on_update(RawSocketHandler.send_raw)

application = tornado.web.Application([
  (r"/", IndexHandler),
  (r"/raw", RawHandler),
  (r"/what-should-i-do", CommandHandler),
  (r'/ws/raw', RawSocketHandler),
  (r'/ws/commands', CommandsSocketHandler),
  (r'/(.*)', tornado.web.StaticFileHandler, {'path': config.static_path }),
])
