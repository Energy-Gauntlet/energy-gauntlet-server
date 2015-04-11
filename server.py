import dotenv
import os
import tornado.ioloop

dotenv.load_dotenv(os.path.dirname(os.path.realpath(__file__)) + "/.env")

from energy_gauntlet.server import application

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
