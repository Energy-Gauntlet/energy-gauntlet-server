from spyrk import SparkCloud
from urlparse import parse_qs
import threading

class Spark():
  """Wrapper class for a spark core device."""

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
    """If this spark is connected then this method will return the raw data from
    the spark's sensors.  Otherwise it will return { 'connected': False }."""
    if self.connected():
      return self._raw
    else:
      return { 'connected': False }

  def connected(self):
    """Returns True if the device represented by this object is connected.  If
    the device is not connected it will check to see if the device is actually
    connected.  This check happens a maximum of every 10 seconds.
    """
    if self._device and self._device.connected:
      return True
    else:
      if not self._connecting:
        self._connecting = True
        threading.Timer(10, self.connect).start()
      self._device = None
      return False

  def update(self):
    """Spawns a thread to retrieve the values from this spark's sensors."""
    thread = threading.Thread(target=self._update)
    thread.start()
    return thread

  def connect(self):
    """Checks the spark cloud API to see if this device is connected."""
    self._device     = self.connection.devices[self.id]
    self._connecting = False

  def _update_var_keys_loop(self):
    """The variables for a given core are cached.  This method updates this
    cache.
    """
    if self.connected():
      threading.Thread(target=self._update_var_keys).start()
    threading.Timer(self.__class__.update_keys_interval, self._update_var_keys_loop).start()

  def _update_var_keys(self):
    try:
      self._var_keys = self._device.variables.keys()
    except Exception as ex:
      pass

  def _update(self):
    """Reads the data from the spark core.  The values can be retrieved via the
    get_raw method."""
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
    if key != 'error_description':
      self._raw[key] = getattr(self._device, key)
