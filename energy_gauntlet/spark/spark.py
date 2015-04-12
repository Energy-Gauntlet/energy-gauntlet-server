from spyrk import SparkCloud
import threading

class Spark:

  def __init__(self, connection, deviceId):
    self.on_update_listeners = set()
    self.raw        = {}
    self.device     = None
    self.id         = deviceId
    self.connection = connection
    self.connect()

  def get_raw(self):
    if self.connected():
      return self.raw
    else:
      return { 'connected': False }

  def connected(self):
    if self.device and self.device.connected:
      return True
    else:
      self.device = None
      return False

  def update(self):
    thread = threading.Thread(target=self._update)
    thread.start()
    return thread

  def connect(self):
    self.device = self.connection.devices[self.id]
    # threading.Thread(target=self._connect)

  def _connect(self):
    self.device = self.connection.devices[self.id]

  def _update(self):
    try:
      d = {}
      for k in self.device.variables.keys():
        d[k] = getattr(self.device, k)
      self.raw = d
    except Exception:
      self.device = None # assume disconnected
      self.raw = {}
