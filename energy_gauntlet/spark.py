import time
import os
from spyrk import SparkCloud
from commands import *
import threading

spark_connection = SparkCloud(os.getenv('ACCESS_TOKEN'))

class Spark:

  def __init__(self, spark_connection):
    self.device = spark_connection.devices['carls']

  def get_raw(self):
    return { 'connected': False } if not self.device.connected else {
      'connected': True,
      'flex0':     self.device.flex0,
      'button0':   self.device.button0,
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

spark = Spark(spark_connection)
