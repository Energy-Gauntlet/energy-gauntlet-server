import os
import time
import tornado.web
from server import handlers, RawSocketHandler, CommandSocketHandler
from spark import Collection, Spark, sparks
from commands import *
from commander import commander

from spyrk import SparkCloud
connection = SparkCloud(os.getenv('TOKEN', ''))
for deviceId in connection.devices:
  sparks.add_spark(Spark(connection, deviceId))

def send_commands(raw):
  commander.update(raw)
  CommandSocketHandler.send(commander.commands)

sparks.on_update(RawSocketHandler.send)
sparks.on_update(send_commands)

application = tornado.web.Application(handlers)
