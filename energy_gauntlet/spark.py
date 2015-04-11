import time
import os
from spyrk import SparkCloud
from commands import *
import threading

class Spark:

  def __init__(self, token):
    self.token = token
    self.connect()

  def connect(self):
    self.connection = SparkCloud(self.token)
    self.device     = self.connection.devices['carls']

  def get_raw(self):
    if not self.device.connected:
      self.connect()
      return {
        'connected': False
      }
    else:
      return {
        'flex_0':   self.device.flex_0,
        'button_0': self.device.button_0,
      }

  # rake raw and do something to figure out what commands to do
  def get_commands(self):
    raw = self.get_raw()
    return [
      [
        PoleUp(),
        PoleStop(),
        PoleDown(),
        PoleStop()
      ][(int(time.time()) % 8) / 2]
    ]

spark = Spark(os.getenv('ACCESS_TOKEN'))
