import os
import time
import tornado.web
from server import handlers, RawSocketHandler, CommandSocketHandler
from spark import Collection, Spark, sparks
from commands import *
from commander import commander

devices = os.getenv('DEVICES', '').split(',')
for device in devices:
  token = os.getenv(device.upper() + '_TOKEN', '')
  sparks.add_spark(Spark(token, device))

def send_commands(raw):
  commander.update(raw)
  CommandSocketHandler.send(commander.commands)

sparks.on_update(RawSocketHandler.send)
sparks.on_update(send_commands)

application = tornado.web.Application(handlers)
