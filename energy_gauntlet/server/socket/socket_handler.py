from tornado.escape import json_encode
import tornado.websocket
import threading

class SocketHandler(tornado.websocket.WebSocketHandler):

  def check_origin(self, origin):
    return True

  def open(self):
    self.__class__.clients.add(self)

  def on_close(self):
    self.__class__.clients.remove(self)

  @classmethod
  def send(cls, data):
    to_send = json_encode(data)
    try:
      for client in cls.clients:
        try:
          # threading.Thread(target=client.write_message, args=(to_send,))
          client.write_message(to_send)
        except:
          pass
    except:
      pass

  @classmethod
  def new(cls, name):
    def __init__(self, arg1, arg2):
      SocketHandler.__init__(self, arg1, arg2)
    newclass = type(name, (SocketHandler,),{"__init__": __init__})
    newclass.clients = set()
    return newclass
