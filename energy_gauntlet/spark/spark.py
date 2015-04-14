from spyrk import SparkCloud
from urlparse import parse_qs
import threading

class Spark():
  update_keys_interval = 10

  def __init__(self, connection, deviceId):
    # Initialize private vars
    self._on_update_listeners = set()
    self._device              = None
    self._connecting          = False
    self._var_keys            = []
    self._raw                 = {}

    # Public vars
    self.id         = deviceId
    self.connection = connection

    # Start attempting to connect
    self.connect()
    # Also start the update var keys loop
    self._update_var_keys_loop()

  def get_raw(self):
    if self.connected():
      return self._raw
    else:
      return { 'connected': False }

  def connected(self):
    if self._device and self._device.connected:
      return True
    else:
      if not self._connecting:
        threading.Thread(target=self.connect).start()
      self._device = None
      return False

  def update(self):
    thread = threading.Thread(target=self._update)
    thread.start()
    return thread

  def connect(self):
    self._device     = self.connection.devices[self.id]
    self._connecting = False

  def _update_var_keys_loop(self):
    if self.connected():
      threading.Thread(target=self._update_var_keys).start()
    threading.Timer(self.__class__.update_keys_interval, self._update_var_keys_loop).start()

  def _update_var_keys(self):
    try:
      self._var_keys = self._device.variables.keys()
    except Exception as ex:
      pass

  def _update(self):
    if self.connected():
      self._raw = {}
      try:
        threads = []
        for key in self._var_keys:
          thread = threading.Thread(target=self._set_raw_for, args=(key,))
          thread.start()
          threads.append(thread)
        for thread in threads:
          thread.join()
      except Exception:
        self._device = None # assume disconnected
        self._raw    = {}

  def _set_raw_for(self, key):
    self._raw[key] = getattr(self._device, key)
