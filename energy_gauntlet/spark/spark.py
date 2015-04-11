from spyrk import SparkCloud
import threading

class Spark:

  def __init__(self, token, deviceId):
    self.on_update_listeners = set()
    self.raw        = {}
    self.token      = token
    self.device     = None
    self.id         = deviceId
    self.connect()

  def connected(self):
    if self.device and self.device.connected:
      return True
    else:
      self.device = None
      return False

  def update(self):
    threading.Thread(target=self._update)

  def connect(self):
    threading.Thread(target=self._connect)

  def _connect(self):
    self.connection = SparkCloud(self.token)
    self.device     = self.connection.devices[self.id]

  def _update(self):
    try:
      d = {}
      for k in self.device.variables.keys():
        d[k] = getattr(self.device, k)
      self.raw = d
    except Exception:
      self.device = None # assume disconnected
      self.raw = {}
