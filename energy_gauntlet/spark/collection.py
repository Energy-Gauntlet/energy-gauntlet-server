import threading

class Collection:

  def __init__(self):
    self.sparks    = set()
    self.listeners = []
    self.raw       = {}
    self._update_loop()

  def add_spark(self, spark):
    self.sparks.add(spark)

  def connected_sparks(self):
    return filter(lambda s: s.connected() ,self.sparks)

  def _update_loop(self):
    raw     = {}
    sparks  = self.connected_sparks()
    threads = []
    for spark in sparks:
      threads.append(spark.update)
    for thread in threads:
      thread.join()
    self.raw = {}
    for spark in sparks:
      self.raw[spark.id] = spark.raw
    for listener in self.listeners:
      listener(self.raw)
    threading.Thread(target=self._update_loop).start()

  def on_update(self, listener):
    self.listeners.append(listener)
