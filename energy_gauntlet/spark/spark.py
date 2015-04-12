from spyrk import SparkCloud
from urlparse import parse_qs
import threading

class Spark():

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

  def _update(self):
    self.raw = {}
    try:
      threads = []
      for k in self.device.variables.keys():
        thread = threading.Thread(target=self._set_raw_for(k))
        thread.start()
        threads.append(thread)
      for thread in threads:
        thread.join()
    except Exception:
      self.device = None # assume disconnected
      self.raw    = {}

  def _set_raw_for(self, key):
    self.raw[key] = getattr(self.device, key)
