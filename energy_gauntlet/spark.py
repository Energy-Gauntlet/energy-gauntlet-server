import time
import os
from spyrk import SparkCloud
from commands import *
import threading

class Spark:

  def __init__(self, token):
    self.token  = token
    self.device = None
    # self.connect()
    self._update_loop()

  def _update_loop(self):
    d = {}
    if self.device and self.device.connected:
      for k in self.device.variables.keys():
        d[k] = getattr(self.device, k)
      self.raw = d
    else:
      self.connect()
      self.raw = { 'connected': False }
    threading.Timer(0.5, self._update_loop).start()

  def connect(self):
    try:
      self.connection = SparkCloud(self.token)
      self.device     = self.connection.devices['carls']
    except Exception:
      pass

  def get_raw(self):
    # d = {}
    # if self.device and self.device.connected:
    #   for k in self.device.variables.keys():
    #     d[k] = getattr(self.device, k)
    #   self.raw = d
    # else:
    #   self.connect()
    #   self.raw = { 'connected': False }
    return self.raw

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
