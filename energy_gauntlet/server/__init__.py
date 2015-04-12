import os
from ..commander import commander
from ..spark import sparks
import tornado.web
from socket.socket_handler import SocketHandler as ws
from tornado.escape import json_encode

static_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../static')

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    with open (os.path.dirname(os.path.realpath(__file__)) + '/../../static/index.html', "r") as indexFile:
      self.write(indexFile.read())

class CommandHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'application/json')
    self.write(json_encode(commander.commands))

class RawHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'application/json')
    self.write(json_encode(sparks.raw))

RawSocketHandler     = ws.new('RawSocketHandler')
CommandSocketHandler = ws.new('CommandSocketHandler')

handlers = [
  (r"/",                 IndexHandler),
  (r"/raw",              RawHandler),
  (r"/what-should-i-do", CommandHandler),
  (r'/ws/raw',           RawSocketHandler),
  (r'/ws/commands',      CommandSocketHandler),
  (r'/(.*)',             tornado.web.StaticFileHandler, {'path': static_path }),
]
