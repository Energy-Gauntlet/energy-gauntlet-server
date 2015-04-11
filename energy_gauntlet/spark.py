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
    try:
      self.connection = SparkCloud(self.token)
      self.device     = self.connection.devices['carls']
    except Exception:
      pass

  def get_raw(self):
    if not self.device.connected:
      self.connect()
      return {
        'connected': False
      }
    else:
      d = {}
      for k in self.device.variables.keys():
        d[k] = getattr(self.device, k)
      return d

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
