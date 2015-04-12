import time
from commands import *

speed_threshold = 0.1

# CALIBRATION
# ---------------
flex0_low = 1440.
flex0_high = 1900.

flex1_low = 1700.
flex1_high = 2100.
# ----------------

def fix_ranges(flex, low, high):
  if flex > high:
    flex = high
  elif flex < low:
    flex = low
  return flex

def speed_turn(flex0, flex1):
  # normalize

  flex0 = fix_ranges(flex0, flex0_low, flex0_high)
  flex1 = fix_ranges(flex1, flex1_low, flex1_high)

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
      
      if speed < speed_threshold:
        return

      self.commands = [variableDrive({ 'forwardBack': speed, 
                                     'leftRight': turn })]

commander = Commander()