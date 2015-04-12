import time
from commands import *

class Commander():

  def __init__(self):
    self.commands = []

  def update(self, raw):
    self.commands = [
      [
        PoleUp(),
        PoleStop(),
        PoleDown(),
        PoleStop()
      ][(int(time.time()) % 8) / 2]
    ]

commander = Commander()
