import os
import time
import tornado.web
from server import handlers, RawSocketHandler, CommandSocketHandler
from spark import Collection, Spark, sparks
from commands import *
from commander import commander
import threading

from spyrk import SparkCloud

def populate_devices():
  token      = os.getenv('TOKEN', '')
  connection = SparkCloud(token)
  for deviceId in connection.devices:
    sparks.add_spark(Spark(connection, deviceId))

threading.Thread(target=populate_devices).start()

def send_commands(raw):
  commander.update(raw)
  CommandSocketHandler.send(commander.commands)

sparks.on_update(RawSocketHandler.send)
sparks.on_update(send_commands)

application = tornado.web.Application(handlers)
