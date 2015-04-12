import time
from commands import *

# CALIBRATION
# ---------------
flex0_low = 1200.
flex0_high = 2000.

flex1_low = 1200.
flex1_high = 2000.
# ----------------

def speed_turn(flex0, flex1):
  # normalize
  flex0 = (flex0 - flex0_low) / (flex0_high - flex0_low)
  flex1 = (flex1 - flex1_low) / (flex1_high - flex1_low)


  m1 = flex0 / (flex0 + flex1)
  m2 = flex1 / (flex0 + flex1)

  turn =  m2 * 2 - 1
  speed = max([flex0, flex1])
  return speed, turn


class Commander():

  def __init__(self):
    self.commands = []

  def update(self, raw):

    right_flex_0 = float(raw['right']['flex_0'])
    right_flex_1 = float(raw['right']['flex_1'])
    right_button = int(raw['right']['button'])

    if right_button > 0:
      speed, turn = speed_turn(flex0, flex1)

    self.commands = [
      [
        PoleUp(),
        PoleStop(),
        PoleDown(),
        PoleStop()
      ][(int(time.time()) % 8) / 2]
    ]

commander = Commander()
