import time
from commands import *
import threading

speed_threshold = 0.25

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

  flex0 = 1 - (flex0 - flex0_low) / (flex0_high - flex0_low)
  flex1 = 1 - (flex1 - flex1_low) / (flex1_high - flex1_low)

  m1 = flex0 / (flex0 + flex1)
  m2 = flex1 / (flex0 + flex1)

  turn =  m2 * 2 - 1
  speed = max([flex0, flex1])

  return speed, turn

class Commander():
  """The Commander class takes raw input from the sparks and creates an array of
  commands for the Double to perform.
  """

  def __init__(self):
    self.commands         = []
    self._commands_to_add = []

  def say(self, text):
    self._commands_to_add.append(Speak({ 'string': text }))

  def clear_additional_commands(self):
    self._commands_to_add = []

  def get_commands(self):
    """Returns the current set of commands the commander wants to give the
    double at this time.
    """
    cmds = self.commands + self._commands_to_add
    threading.Timer(1, self.clear_additional_commands).start();
    return cmds

  def update(self, raw):
    """Takes raw data from sparks and sets a commands instance variable to an
    array of command objects which will later be sent to the double robot to
    perform.
    """
    if not ('right' in raw['sparks'] and 'connected' in raw['sparks']['right']):
      self.commands = [VariableDrive({ 'forwardBack': 0.0,
                                       'leftRight': 0.0 })]

      try:
        right_flex_0 = float(raw['sparks']['right']['flex_0'])
        right_flex_1 = float(raw['sparks']['right']['flex_1'])
        right_button = int(raw['sparks']['right']['button_0'])


        speed, turn = speed_turn(right_flex_0, right_flex_1)

        #print speed, turn
        if speed < speed_threshold:
          return

        if right_button > 0:
          speed = - speed
        self.commands = [VariableDrive({ 'forwardBack': speed,
                                       'leftRight': turn })]
      except:
        pass

commander = Commander()
