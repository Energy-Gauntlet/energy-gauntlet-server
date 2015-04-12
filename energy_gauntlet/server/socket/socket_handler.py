from tornado.escape import json_encode
import tornado.websocket

class SocketHandler(tornado.websocket.WebSocketHandler):

  def check_origin(self, origin):
    return True

  def open(self):
    self.__class__.clients.add(self)

  def on_close(self):
    self.__class__.clients.remove(self)

  @classmethod
  def send(cls, data):
    for clients in cls.clients:
      try:
          clients.write_message(json_encode(data))
      except:
        pass

  @classmethod
  def new(cls, name):
    def __init__(self, arg1, arg2):
      SocketHandler.__init__(self, arg1, arg2)
    newclass = type(name, (SocketHandler,),{"__init__": __init__})
    newclass.clients = set()
    return newclass
