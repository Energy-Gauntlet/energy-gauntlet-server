import os
from spyrk import SparkCloud
from commands import *
import threading

spark_client = None # SparkCloud(os.getenv('ACCESS_TOKEN'))

class Spark:

  def __init__(self, spark_client = None):
    self.client = spark_client

  def get_raw(self):
    return {
      'leftFinger': 50 #self.client.analogread('A0')
    }

  # rake raw and do something to figure out what commands to do
  def get_commands(self):
    raw = self.get_raw()
    return [Drive()]

spark = Spark(spark_client)
