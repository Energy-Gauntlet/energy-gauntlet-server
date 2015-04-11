import os
import tornado.web
from server import handlers, RawSocketHandler, CommandSocketHandler
from spark import Collection, Spark

sparks = Collection()

sparks.add_spark(Spark(os.getenv('ACCESS_TOKEN'), 'carls'))

sparks.on_update(RawSocketHandler.send)

application = tornado.web.Application(handlers)
