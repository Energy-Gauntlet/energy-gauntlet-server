from time import time
import threading

class Collection:

  def __init__(self, interval):
    self._sparks   = set()
    self.listeners = []
    self.raw       = {}
    self.interval  = interval
    self._update_loop()

  def add_spark(self, spark):
    self._sparks.add(spark)

  def connected_sparks(self):
    return filter(lambda s: s.connected() ,self._sparks)

  def _update_loop(self):
    raw     = {}
    threads = []
    latency = int(round(time() * 1000))
    for spark in self.connected_sparks():
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
    for listener in self.listeners:
      listener(self.raw)
    threading.Timer(self.interval, self._update_loop).start()

  def on_update(self, listener):
    self.listeners.append(listener)
