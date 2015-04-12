import os
import time
import tornado.web
from server import handlers, RawSocketHandler, CommandSocketHandler
from spark import Collection, Spark
from commands import *

sparks = Collection(0.2)

devices = os.getenv('DEVICES').split(',')
for device in devices:
  token = os.getenv(device.upper() + '_TOKEN')
  sparks.add_spark(Spark(token, device))

def testing_commands_generator():
  return [
    [
      PoleUp(),
      PoleStop(),
      PoleDown(),
      PoleStop()
    ][(int(time.time()) % 8) / 2]
  ]

def get_commands(raw):
  CommandSocketHandler.send(testing_commands_generator())

sparks.on_update(RawSocketHandler.send)
sparks.on_update(get_commands)

application = tornado.web.Application(handlers)
