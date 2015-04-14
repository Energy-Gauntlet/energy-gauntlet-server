from time import time
import threading

class Collection:

  def __init__(self, interval = 0):
    self._sparks_access = threading.Lock()
    self._sparks        = set()
    self._listeners     = []

    self.raw            = {}
    self.interval       = interval

    self._update_loop()

  def add_spark(self, spark):
    with self._sparks_access:
      self._sparks.add(spark)

  def _update_loop(self):
    raw     = {}
    threads = []
    latency = int(round(time() * 1000))
    with self._sparks_access:
      for spark in self._sparks:
        threads.append(spark.update())
      for thread in threads:
        thread.join()
      latency  = int(round(time() * 1000)) - latency
      self.raw = {
        'latency':  latency,
        'interval': self.interval * 1000,
        'sparks':   {}
      }
      for spark in self._sparks:
        self.raw['sparks'][spark.id] = spark.get_raw()
      for listener in self._listeners:
        listener(self.raw)
      threading.Timer(self.interval, self._update_loop).start()

  def on_update(self, listener):
    self._listeners.append(listener)
